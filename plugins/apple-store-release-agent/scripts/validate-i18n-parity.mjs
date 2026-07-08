#!/usr/bin/env node
// validate-i18n-parity.mjs — locale key parity (pt/en/es) + hardcoded-string hint.
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve, extname } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

// Discover locale files. Common conventions.
const LOCALE_DIRS = ["locales", "i18n", "i18n/locales", "src/locales", "src/i18n", "translations"];
const LOCALE_FILES = [
  { re: /^pt(-br)?\.json$/i, lang: "pt" },
  { re: /^pt(-br)?\.(ts|js)$/i, lang: "pt", code: true },
  { re: /^en(-us)?\.json$/i, lang: "en" },
  { re: /^en(-us)?\.(ts|js)$/i, lang: "en", code: true },
  { re: /^es(-es)?\.json$/i, lang: "es" },
  { re: /^es(-es)?\.(ts|js)$/i, lang: "es", code: true },
];

const locales = {}; // lang -> keySet
function matchLocale(file) {
  for (const def of LOCALE_FILES) if (def.re.test(file)) return def;
  return null;
}
function walk(dir) {
  let entries = [];
  try { entries = readdirSync(dir); } catch { return; }
  for (const e of entries) {
    const p = join(dir, e);
    let st;
    try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) walk(p);
    else {
      const def = matchLocale(e);
      if (!def) continue;
      const keys = extractKeys(p, def.code);
      if (!locales[def.lang]) locales[def.lang] = { files: [], keys: new Set() };
      locales[def.lang].files.push(p);
      for (const k of keys) locales[def.lang].keys.add(k);
    }
  }
}
for (const d of LOCALE_DIRS) walk(join(project, d));

const langs = Object.keys(locales);

if (langs.length === 0) {
  add(args.strict ? "WARNING" : "INFO", "i18n", "No locale files (pt/en/es) found; i18n parity skipped.", null);
} else {
  // Compare key sets pairwise.
  const ref = langs[0];
  const refKeys = [...locales[ref].keys];
  for (const lang of langs.slice(1)) {
    const other = locales[lang].keys;
    const missing = refKeys.filter((k) => !other.has(k));
    const orphan = [...other].filter((k) => !locales[ref].keys.has(k));
    for (const k of missing) {
      add(args.strict ? "BLOCKER" : "WARNING", "i18n-parity", `Missing key "${k}" in ${lang} (vs ${ref}).`, locales[lang].files.join(","));
    }
    for (const k of orphan) {
      add(args.strict ? "BLOCKER" : "WARNING", "i18n-parity", `Orphan key "${k}" in ${lang} (not in ${ref}).`, locales[lang].files.join(","));
    }
  }
  const want = ["pt", "en", "es"];
  for (const w of want) {
    if (!langs.includes(w)) add("WARNING", "i18n-coverage", `Locale ${w} not found.`, null);
  }
}

// Hardcoded strings hint in presentation layer (best-effort, shallow).
const SRC = join(project, "src/presentation");
if (existsSync(SRC)) {
  const SUSPECT = />\s*[A-ZÀ-Ú][a-zà-ú]{4,}\s+[a-zà-ú]{2,}</;
  let scanned = 0;
  (function walkSrc(dir) {
    let entries = [];
    try { entries = readdirSync(dir); } catch { return; }
    for (const e of entries) {
      const p = join(dir, e);
      let st; try { st = statSync(p); } catch { continue; }
      if (st.isDirectory()) walkSrc(p);
      else if (/\.(tsx|jsx)$/.test(e) && scanned < 200) {
        scanned++;
        const text = readFileSync(p, "utf8");
        const lines = text.split("\n");
        for (let i = 0; i < lines.length; i++) {
          if (SUSPECT.test(lines[i])) {
            add("INFO", "i18n-hardcoded", `Possible hardcoded copy: ${lines[i].trim().slice(0, 80)}`, p, i + 1);
            break; // one hint per file to limit noise
          }
        }
      }
    }
  })(SRC);
}

const decision = decide(findings);
const report = render(findings, decision, project);
if (args.output) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(resolve(args.output), report, "utf8");
} else if (!args.json) console.log(report);
if (args.json) console.log(JSON.stringify({ project, decision, findings }, null, 2));
process.exit(decision === "NO_GO" ? 1 : 0);

function extractKeys(file, isCode) {
  const keys = new Set();
  const text = readFileSync(file, "utf8");
  if (isCode) {
    // quoted keys like key: "value" or 'key': "value"
    const re = /["']([A-Za-z0-9_.-]+)["']\s*:\s*["']/g;
    let m;
    while ((m = re.exec(text))) keys.add(m[1]);
  } else {
    try {
      const obj = JSON.parse(text);
      flatten(obj, "", keys);
    } catch {
      add("WARNING", "i18n", `Failed to parse JSON locale ${file}.`, file);
    }
  }
  return keys;
}
function flatten(obj, prefix, set) {
  for (const [k, v] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === "object" && !Array.isArray(v)) flatten(v, path, set);
    else set.add(path);
  }
}
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
  lines.push("# i18n Parity Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push("| Severity | Area | Message | File:Line |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"}${f.line ? ":" + f.line : ""} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
