#!/usr/bin/env node
// validate-no-policy-risk-copy.mjs
// Scans metadata, locale files, and presentation text for policy-risk copy.
// Classifies LOW / MEDIUM / HIGH and suggests safer wording.
// Flags: --project <path>  --output <path>  --strict  --json

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--project') out.project = argv[++i];
    else if (a === '--output') out.output = argv[++i];
    else if (a === '--strict') out.strict = true;
    else if (a === '--json') out.json = true;
  }
  return out;
}

const add = (level, code, message, file = null) => findings.push({ level, code, message, file });

// HIGH = direct gambling/money-guarantee. MEDIUM = suggestive. LOW = borderline.
const TERMS = [
  { re: /\bapost(?:a|ar|e)\b/i, level: 'HIGH', safe: 'compita / participe' },
  { re: /\bbetting\b/i, level: 'HIGH', safe: 'compete / play' },
  { re: /\bgambling\b/i, level: 'HIGH', safe: 'play / compete' },
  { re: /casino/i, level: 'HIGH', safe: '(remove casino language)' },
  { re: /cashout\s+garantido/i, level: 'HIGH', safe: '(remove — no guaranteed withdrawal)' },
  { re: /saque\s+garantido/i, level: 'HIGH', safe: '(remove — no guaranteed withdrawal)' },
  { re: /ganhe\s+dinheiro/i, level: 'HIGH', safe: 'jogue / organize seus jogos' },
  { re: /lucro\s+garantido|renda\s+garantida/i, level: 'HIGH', safe: '(remove guaranteed income/profit language)' },
  { re: /dinheiro\s+fácil/i, level: 'HIGH', safe: '(remove easy-money language)' },
  { re: /prêmio\s+garantido/i, level: 'MEDIUM', safe: 'recompensas em app (virtual, sem valor real)' },
  { re: /\blucro\b/i, level: 'MEDIUM', safe: '(remove profit wording in non-monetization context)' },
  { re: /cashout/i, level: 'MEDIUM', safe: '(remove withdrawal language)' },
  { re: /saque\s+(instantâneo|imediato|rápido)/i, level: 'MEDIUM', safe: '(remove fast-withdrawal language)' },
  { re: /apostas?\s+(esportivas|desportivas)/i, level: 'HIGH', safe: 'acompanhe / acompanhe partidas' },
  { re: /odds?\s+(garantidas|fixas)/i, level: 'HIGH', safe: '(remove guaranteed-odds language)' },
  { re: /jackpot/i, level: 'HIGH', safe: '(remove jackpot language)' },
  { re: /roleta|caça-níqueis|slot\s+machine/i, level: 'HIGH', safe: '(remove gambling-game language)' },
  { re: /multiplique\s+(seu\s+)?(dinheiro|coins)/i, level: 'MEDIUM', safe: '(remove money-multiplier language)' },
];

function readText(p) { if (!existsSync(p)) return null; try { return readFileSync(p, 'utf8'); } catch { return null; } }

function collectFiles() {
  const out = [];
  const roots = ['metadata', 'store', 'play-store', 'locales', 'i18n', 'src/presentation', 'src/screens', 'src/ui', 'app'];
  for (const r of roots) { const root = join(project, r); if (existsSync(root)) walk(root, out); }
  // locale JSON roots
  for (const r of ['locales', 'i18n/locales', 'src/locales']) { const root = join(project, r); if (existsSync(root)) walk(root, out); }
  return out;
}
function walk(dir, out) {
  try { for (const e of readdirSync(dir, { withFileTypes: true })) { const full = join(dir, e.name); if (e.isDirectory()) walk(full, out); else if (/\.(md|txt|json|tsx|jsx|ts|js)$/i.test(e.name)) out.push(full); } } catch { /* ignore */ }
}

const files = collectFiles();
let scanned = 0;
for (const f of files) {
  const txt = readText(f);
  if (!txt) continue;
  scanned++;
  for (const t of TERMS) {
    t.re.lastIndex = 0;
    const m = txt.match(t.re);
    if (m) add(t.level, 'POLICY_RISK_COPY', `Term "${m[0]}" (risk: ${t.level}). Safer wording: "${t.safe}".`, f.replace(project + '/', ''));
  }
}

const blockers = findings.filter(f => f.level === 'HIGH');
const warns = findings.filter(f => f.level === 'MEDIUM');

function md() {
  const L = ['# Policy Risk Copy Report', '', `Project: \`${project}\``, '',
    `## Scanned ${scanned} file(s)`, '',
    `## Findings — ${blockers.length} HIGH, ${warns.length} MEDIUM, ${findings.filter(f => f.level === 'LOW').length} LOW`, ''];
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}`);
  if (!findings.length) L.push('- No policy-risk copy detected. ✅');
  L.push('', '## Notes', '',
    '- HIGH = likely policy violation. Remove before submission.',
    '- MEDIUM = suggestive; review in context.',
    '- Keyword scan is heuristic; a human must confirm context.', '');
  return L.join('\n');
}

const out = args.json ? JSON.stringify({ project, scanned, findings }, null, 2) : md();
if (args.output) writeOut(args.output, out); else console.log(out);
function writeOut(path, content) { import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8')); }
// --strict fails on HIGH; MEDIUM only warns unless combined
if (args.strict && blockers.length > 0) process.exit(1);
