#!/usr/bin/env node
// validate-app-store-metadata.mjs — App Store metadata presence + risky-word scan.
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

// Risky wording (case-insensitive substrings) — BLOCKER in metadata.
const RISKY = [
  "aposta", "apostar", "betting", "gambling", "cashout garantido",
  "ganhe dinheiro", "lucro", "renda garantida", "saque garantido",
  "withdraw money", "guaranteed income", "earn money", "cash out",
];
const SAFE_SUGGESTIONS = {
  aposta: "use 'organize / match / game' framing (no betting)",
  apostar: "use 'play / join' framing (no betting)",
  betting: "remove; describe as non-monetary sport content",
  gambling: "remove; describe as non-monetary sport content",
  "cashout garantido": "remove; coins are non-withdrawable virtual currency",
  "ganhe dinheiro": "remove; app does not pay users",
  lucro: "remove; do not imply profit/income",
  "renda garantida": "remove; do not imply guaranteed income",
  "saque garantido": "remove; coins cannot be withdrawn",
  "withdraw money": "remove; coins cannot be withdrawn",
  "guaranteed income": "remove; do not imply guaranteed income",
  "earn money": "remove; app does not pay users",
  "cash out": "remove; coins cannot be cashed out",
};

function scanText(text, file) {
  const lower = text.toLowerCase();
  const seen = new Set();
  for (const term of RISKY) {
    if (seen.has(term)) continue;
    const idx = lower.indexOf(term);
    if (idx !== -1) {
      seen.add(term);
      const lineNo = text.slice(0, idx).split("\n").length;
      const suggest = SAFE_SUGGESTIONS[term] || "rephrase with safe, non-monetary wording";
      add("BLOCKER", "wording-risk", `Risky term "${term}". Suggest: ${suggest}.`, file, lineNo);
    }
  }
}

// Metadata search: ./metadata, ./app-store, ./fastlane/metadata, ./store
const metaDirs = ["metadata", "app-store", "store", "fastlane/metadata"];
const metaFiles = new Set();
for (const d of metaDirs) {
  const dp = join(project, d);
  if (existsSync(dp) && statSync(dp).isDirectory()) collectMd(dp);
}
function collectMd(dir) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    const st = statSync(p);
    if (st.isDirectory()) collectMd(p);
    else if (/\.(md|txt|json)$/.test(e)) metaFiles.add(p);
  }
}

// Also scan top-level description files if no metadata dir.
if (metaFiles.size === 0) {
  for (const f of readdirSync(project)) {
    if (/description|keywords|release.?notes|review.?notes/i.test(f) && /\.(md|txt)$/i.test(f)) {
      metaFiles.add(join(project, f));
    }
  }
}

const expected = ["description", "keywords", "release notes", "review notes"];
const present = { description: false, keywords: false, "release notes": false, "review notes": false };

if (metaFiles.size === 0) {
  add(args.strict ? "WARNING" : "INFO", "metadata", "No metadata folder/files detected. Static scan skipped.", null);
} else {
  for (const f of metaFiles) {
    const text = readFileSync(f, "utf8");
    const base = f.toLowerCase();
    if (/description/.test(base)) present.description = true;
    if (/keyword/.test(base)) present.keywords = true;
    if (/release.?notes|whatsnew|changelog/.test(base)) present["release notes"] = true;
    if (/review.?notes|reviewer/.test(base)) present["review notes"] = true;
    scanText(text, f);
  }
  for (const k of expected) {
    if (!present[k]) add("WARNING", "metadata", `Missing ${k} in metadata.`, null);
  }
}

// Screenshots hint
const shotDirs = ["screenshots", "fastlane/screenshots", "metadata/screenshots"];
let hasShots = false;
for (const d of shotDirs) {
  const dp = join(project, d);
  if (existsSync(dp) && statSync(dp).isDirectory()) {
    if (readdirSync(dp).length) hasShots = true;
  }
}
if (!hasShots) add("WARNING", "screenshots", "No screenshots folder found (Apple requires shipping-build screenshots).", null);

const decision = decide(findings);
const report = render(findings, decision, project);
if (args.output) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(resolve(args.output), report, "utf8");
} else if (!args.json) console.log(report);
if (args.json) console.log(JSON.stringify({ project, decision, findings }, null, 2));
process.exit(decision === "NO_GO" ? 1 : 0);

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
  lines.push("# App Store Metadata Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push("| Severity | Area | Message | File:Line |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"}${f.line ? ":" + f.line : ""} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
