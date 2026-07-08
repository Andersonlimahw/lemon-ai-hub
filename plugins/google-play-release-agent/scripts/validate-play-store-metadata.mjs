#!/usr/bin/env node
// validate-play-store-metadata.mjs
// Play Store listing readiness + risky-term scan.
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

const RISKY = [
  { term: /\bapost(?:a|ar)\b/i, safe: 'compita / participe (no real-money payout)' },
  { term: /\bbetting\b/i, safe: 'compete / play' },
  { term: /\bgambling\b/i, safe: 'play / compete' },
  { term: /cashout\s+garantido/i, safe: '(remove — no guaranteed withdrawal language)' },
  { term: /ganhe\s+dinheiro/i, safe: 'jogue / organize seus jogos' },
  { term: /\blucro\b/i, safe: '(remove profit language for non-monetization context)' },
  { term: /renda\s+garantida/i, safe: '(remove guaranteed-income language)' },
  { term: /saque\s+garantido/i, safe: '(remove guaranteed-withdrawal language)' },
  { term: /dinheiro\s+fácil/i, safe: '(remove easy-money language)' },
  { term: /prêmio\s+garantido/i, safe: 'recompensas em app (virtual, sem valor real)' },
];

function readText(p) {
  if (!existsSync(p)) return null;
  try { return readFileSync(p, 'utf8'); } catch { return null; }
}

function findMetadataFiles() {
  // common conventions: metadata/ , store/ , play-store/
  const dirs = ['metadata', 'store', 'play-store', 'store-listing', 'fastlane/metadata/android'];
  const found = [];
  for (const d of dirs) {
    const root = join(project, d);
    if (existsSync(root)) found.push({ dir: d, files: listDeep(root) });
  }
  return found;
}

function listDeep(dir) {
  const out = [];
  try {
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, e.name);
      if (e.isDirectory()) out.push(...listDeep(full));
      else out.push(full);
    }
  } catch { /* ignore */ }
  return out;
}

function checkListing(md) {
  const txt = (s) => (s == null ? '' : String(s));
  const all = md.map(m => m.files.map(f => ({ f, txt: readText(f) || '' }))).flat();
  const joined = all.map(a => a.txt).join('\n');

  const hasShort = /short[_\s-]?desc/i.test(joined) || all.some(a => /short/i.test(a.f));
  const hasFull = /full[_\s-]?desc/i.test(joined) || all.some(a => /full/i.test(a.f));
  const hasNotes = /release[_\s-]?notes?/i.test(joined) || all.some(a => /changelogs?/i.test(a.f));
  const hasShots = all.some(a => /\.(png|jpg|jpeg|webp)$/i.test(a.f));

  if (md.length === 0) add('WARN', 'NO_METADATA_DIR', 'No metadata/store-listing directory found. Provide Play Store listing (title, short/full desc, screenshots).', null);
  if (!hasShort) add('WARN', 'NO_SHORT_DESC', 'Short description (≤80 chars) not detected.', null);
  if (!hasFull) add('WARN', 'NO_FULL_DESC', 'Full description (≤4000 chars) not detected.', null);
  if (!hasNotes) add('INFO', 'NO_RELEASE_NOTES', 'No release notes / changelog detected. Generate via release-notes template.', null);
  if (!hasShots) add('WARN', 'NO_SCREENSHOTS', 'No screenshots detected (min 2, max 8 per type).', null);

  // risky-term scan on every text file
  for (const a of all) {
    for (const r of RISKY) {
      const m = a.txt.match(r.term);
      if (m) add('HIGH', 'RISKY_TERM', `Risky term "${m[0]}" detected. Suggest safer wording: "${r.safe}".`, a.f.replace(project + '/', ''));
    }
  }
}

checkListing(findMetadataFiles());

const errors = findings.filter(f => f.level === 'ERROR' || f.level === 'HIGH');
const warns = findings.filter(f => f.level === 'WARN');
const verdict = errors.length ? 'NO_GO' : (warns.length ? 'GO_WITH_WARNINGS' : 'GO');

function md() {
  const L = ['# Play Store Metadata Report', '', `Project: \`${project}\``, '',
    `## Summary — ${errors.length} blocker(s), ${warns.length} warning(s)`, ''];
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}${f.file ? ` (\`${f.file}\`)` : ''}`);
  L.push('', `## Verdict — **${verdict}**`, '');
  return L.join('\n');
}

if (args.json) {
  const out = JSON.stringify({ project, findings, verdict }, null, 2);
  if (args.output) writeOut(args.output, out); else console.log(out);
} else {
  const out = md();
  if (args.output) writeOut(args.output, out); else console.log(out);
}

function writeOut(path, content) {
  import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8'));
}

if (args.strict && (errors.length > 0 || warns.length > 0)) process.exit(1);
