#!/usr/bin/env node
// validate-no-native-alerts.mjs — find Alert.alert / Alert.prompt usages.
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

const RE = /\bAlert\.(alert|prompt)\s*\(/g;
const SKIP = /[\\/](node_modules|\.git|dist|build|coverage)[\\/]/;
const EXT = /\.(tsx|ts|jsx|js)$/;

let scanned = 0;
let hits = 0;
(function walk(dir) {
  let entries = [];
  try { entries = readdirSync(dir); } catch { return; }
  for (const e of entries) {
    if (e === "node_modules" || e === ".git" || e === "dist" || e === "build") continue;
    const p = join(dir, e);
    let st; try { st = statSync(p); } catch { continue; }
    if (SKIP.test(p)) continue;
    if (st.isDirectory()) walk(p);
    else if (EXT.test(e) && scanned < 1000) {
      scanned++;
      const text = readFileSync(p, "utf8");
      const lines = text.split("\n");
      for (let i = 0; i < lines.length; i++) {
        if (RE.test(lines[i])) {
          RE.lastIndex = 0;
          hits++;
          add(args.strict ? "WARNING" : "INFO", "native-alert",
            `Alert.${/prompt/.test(lines[i]) ? "prompt" : "alert"} used — prefer confirmation sheet / snackbar abstraction.`,
            p, i + 1);
        }
      }
    }
  }
})(project);

if (hits === 0) {
  add("INFO", "native-alert", "No Alert.alert/Alert.prompt usages found.", null);
} else if (hits > 5) {
  add("WARNING", "native-alert", `${hits} native alert(s) found — consider a shared confirmation/sheet abstraction for review UX.`, null);
}

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
  lines.push("# Native Alert Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push("| Severity | Area | Message | File:Line |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"}${f.line ? ":" + f.line : ""} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
