#!/usr/bin/env node
// validate-ios-release.mjs — static iOS/Expo/EAS release readiness audit.
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const strict = args.strict;
const out = args.output;

const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

// --- app.json / app.config.* ---
function loadAppConfig() {
  const candidates = ["app.json", "app.config.json", "app.config.js", "app.config.ts"];
  for (const c of candidates) {
    const p = join(project, c);
    if (!existsSync(p)) continue;
    if (c.endsWith(".json")) {
      try {
        const raw = readFileSync(p, "utf8");
        const parsed = JSON.parse(raw);
        return { file: p, config: parsed.expo || parsed, raw };
      } catch {
        add("WARNING", "app-config", `Failed to parse ${c}`, p);
        return { file: p, config: {}, raw: "" };
      }
    }
    // app.config.{js,ts}: best-effort, do not execute. Grep for keys.
    const raw = readFileSync(p, "utf8");
    return { file: p, config: extractFromConfigSrc(raw), raw };
  }
  return null;
}

function extractFromConfigSrc(src) {
  const cfg = {};
  const bid = src.match(/bundleIdentifier\s*:\s*['"]([^'"]+)['"]/);
  if (bid) cfg.bundleIdentifier = bid[1];
  const name = src.match(/\bname\s*:\s*['"]([^'"]+)['"]/);
  if (name) cfg.name = name[1];
  const sl = src.match(/slug\s*:\s*['"]([^'"]+)['"]/);
  if (sl) cfg.slug = sl[1];
  const ver = src.match(/\bversion\s*:\s*['"]([^'"]+)['"]/);
  if (ver) cfg.version = ver[1];
  return cfg;
}

const app = loadAppConfig();
if (!app) {
  add(strict ? "BLOCKER" : "WARNING", "app-config", "No app.json / app.config.* found (not an Expo app?).", null);
} else {
  if (!app.config.bundleIdentifier) {
    add("BLOCKER", "bundle-id", "ios.bundleIdentifier missing.", app.file);
  } else if (/^com\.example|yourdomain|changeme|placeholder/i.test(app.config.bundleIdentifier)) {
    add("BLOCKER", "bundle-id", `bundleIdentifier looks placeholder: ${app.config.bundleIdentifier}`, app.file);
  } else if (!/^[a-z0-9-]+(\.[a-z0-9-]+)+$/i.test(app.config.bundleIdentifier)) {
    add("WARNING", "bundle-id", `bundleIdentifier not reverse-DNS: ${app.config.bundleIdentifier}`, app.file);
  }
  if (!app.config.version) add("WARNING", "version", "App version missing in config.", app.file);
  // infoPlist / usage strings when native modules implied
  const raw = String(app.raw || "");
  const wantsCamera = /expo-camera|expo-image-picker|RCTCamera/.test(raw) || existsSync(join(project, "node_modules/expo-camera"));
  const wantsLocation = /expo-location/.test(raw) || existsSync(join(project, "node_modules/expo-location"));
  if (wantsCamera && !/NSCameraUsageDescription|NSPhotoLibraryUsageDescription/.test(raw)) {
    add("WARNING", "infoplist", "Camera/Photo usage likely required but no usage description found in config.", app.file);
  }
  if (wantsLocation && !/NSLocationWhenInUseUsageDescription|NSLocationAlwaysUsageDescription/.test(raw)) {
    add("WARNING", "infoplist", "Location usage likely required but no usage description found in config.", app.file);
  }
}

// --- eas.json ---
const easPath = join(project, "eas.json");
if (!existsSync(easPath)) {
  add(strict ? "BLOCKER" : "WARNING", "eas", "eas.json missing.", null);
} else {
  let eas = {};
  try {
    eas = JSON.parse(readFileSync(easPath, "utf8"));
  } catch {
    add("BLOCKER", "eas", "eas.json is invalid JSON.", easPath);
  }
  const buildProfiles = eas.build || {};
  const submitProfiles = eas.submit || {};
  const prodBuild = buildProfiles.production;
  if (!prodBuild) add("WARNING", "eas", "No 'production' build profile in eas.json.", easPath);
  else {
    if (/development|dev-client|internal/i.test(JSON.stringify(prodBuild))) {
      add("WARNING", "eas", "production build profile may include dev settings.", easPath);
    }
  }
  if (Object.keys(submitProfiles).length === 0) {
    add("INFO", "eas", "No submit profiles in eas.json (submit may use defaults).", easPath);
  }
  if (!prodBuild || !/production/i.test(JSON.stringify(prodBuild))) {
    add("INFO", "eas", "Confirm production profile targets the release channel.", easPath);
  }
}

// --- package.json ---
const pkgPath = join(project, "package.json");
if (!existsSync(pkgPath)) {
  add(strict ? "BLOCKER" : "WARNING", "package", "package.json missing (not a JS/RN project?).", null);
} else {
  let pkg = {};
  try {
    pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
  } catch {
    add("BLOCKER", "package", "package.json is invalid JSON.", pkgPath);
  }
  const scripts = pkg.scripts || {};
  const hasLint = Boolean(scripts.lint);
  const hasTest = Boolean(scripts.test && scripts.test !== "echo \"Error: no test specified\" && exit 1");
  const hasTypecheck = /tsc|typecheck|type-check/.test(JSON.stringify(scripts));
  if (!hasLint) add("WARNING", "quality-gate", "No 'lint' script in package.json.", pkgPath);
  if (!hasTest) add("WARNING", "quality-gate", "No real 'test' script in package.json.", pkgPath);
  if (!hasTypecheck) add("INFO", "quality-gate", "No typecheck script detected.", pkgPath);
  // mock flag scan
  const scanMock = (text) => /EXPO_PUBLIC_USE_MOCK\s*[:=]\s*['"]?true/i.test(text);
  for (const f of [".env.production", ".env", ".env.local"]) {
    const envp = join(project, f);
    if (existsSync(envp)) {
      const envText = readFileSync(envp, "utf8");
      if (scanMock(envText)) {
        add("BLOCKER", "mock-flag", `EXPO_PUBLIC_USE_MOCK=true found in ${f} — must be false for production.`, envp);
      }
    }
  }
}

// --- secrets hygiene (names only, never values) ---
for (const f of ["GoogleService-Info.plist", "google-services.json"]) {
  const p = join(project, f);
  if (existsSync(p)) add("WARNING", "secrets", `${f} present at repo root — ensure it is gitignored, not committed.`, p);
}

const decision = decide(findings);
const report = render(findings, decision, project);

if (out) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(resolve(out), report, "utf8");
} else if (!args.json) {
  console.log(report);
}
if (args.json) console.log(JSON.stringify({ project, decision, findings }, null, 2));

process.exit(decision === "NO_GO" ? 1 : 0);

// ---------- helpers ----------
function parseArgs(argv) {
  const a = {};
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === "--strict") a.strict = true;
    else if (k === "--json") a.json = true;
    else if (k === "--project") a.project = argv[++i];
    else if (k === "--output") a.output = argv[++i];
  }
  return a;
}
function decide(list) {
  if (list.some((f) => f.severity === "BLOCKER")) return "NO_GO";
  if (list.some((f) => f.severity === "WARNING")) return "GO_WITH_WARNINGS";
  return "GO";
}
function render(list, decision, project) {
  const lines = [];
  lines.push("# iOS Release Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push("| Severity | Area | Message | File |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
