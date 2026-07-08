#!/usr/bin/env node
// validate-i18n-parity.mjs
// Compares PT/EN/ES locale files: missing keys, orphan keys, obvious hardcoded strings.
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

const TARGETS = ['pt-BR', 'pt', 'en-US', 'en', 'es-ES', 'es'];
const LOCALE_DIRS = ['locales', 'i18n/locales', 'src/locales', 'translations', 'app/locales'];

function readJson(p) { if (!existsSync(p)) return null; try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; } }
function readText(p) { if (!existsSync(p)) return null; try { return readFileSync(p, 'utf8'); } catch { return null; } }

function findLocales() {
  const found = {};
  for (const d of LOCALE_DIRS) {
    const root = join(project, d);
    if (!existsSync(root)) continue;
    for (const t of TARGETS) {
      const candidates = [`${t}.json`, `${t}.ts`];
      for (const c of candidates) {
        const p = join(root, c);
        if (existsSync(p) && !found[t]) found[t] = p;
      }
    }
  }
  return found;
}

function flattenKeys(obj, prefix = '', out = new Set()) {
  if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
    for (const k of Object.keys(obj)) flattenKeys(obj[k], prefix ? `${prefix}.${k}` : k, out);
  } else {
    out.add(prefix);
  }
  return out;
}

const localeFiles = findLocales();
const locales = Object.keys(localeFiles);
if (locales.length === 0) {
  add('WARN', 'NO_LOCALES', 'No PT/EN/ES locale files found in common dirs (locales/, i18n/locales/, ...).', null);
} else {
  const keysByLocale = {};
  for (const loc of locales) {
    const data = readJson(localeFiles[loc]);
    if (!data) { add('WARN', 'LOCALE_NOT_JSON', `${loc}: file is not valid JSON (dynamic .ts?).`, localeFiles[loc]); continue; }
    keysByLocale[loc] = flattenKeys(data);
  }

  const reference = locales[0];
  const refKeys = keysByLocale[reference] || new Set();

  for (const loc of locales) {
    if (loc === reference) continue;
    const ks = keysByLocale[loc];
    if (!ks) continue;
    const missing = [...refKeys].filter(k => !ks.has(k));
    const orphan = [...ks].filter(k => !refKeys.has(k));
    for (const k of missing) add('WARN', 'MISSING_KEY', `${loc}: missing key "${k}"`, localeFiles[loc]);
    for (const k of orphan) add('INFO', 'ORPHAN_KEY', `${loc}: orphan key "${k}" (not in ${reference})`, localeFiles[loc]);
  }
  // completeness score
  for (const loc of locales) {
    const ks = keysByLocale[loc];
    if (!ks || !refKeys.size) continue;
    const pct = Math.round((ks.size / refKeys.size) * 100);
    add('INFO', 'COMPLETENESS', `${loc}: ${ks.size}/${refKeys.size} keys (${pct}%)`, localeFiles[loc]);
  }
}

// hardcoded strings heuristic in src/presentation
function checkHardcoded() {
  const root = join(project, 'src', 'presentation');
  if (!existsSync(root)) return;
  const files = walk(root);
  for (const f of files) {
    const txt = readText(f);
    if (!txt) continue;
    // JSX text with Portuguese/English lowercase words (very rough)
    const re = />\s*([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s]{4,})\s*</g;
    let m, count = 0;
    while ((m = re.exec(txt)) !== null) { count++; if (count > 3) break; }
    if (count > 0) add('INFO', 'POSSIBLE_HARDCODED', `~${count} candidate hardcoded JSX string(s). Review for i18n.`, f.replace(project + '/', ''));
  }
}
function walk(dir, out = []) {
  try {
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, e.name);
      if (e.isDirectory()) walk(full, out);
      else if (/\.(tsx|jsx)$/i.test(e.name)) out.push(full);
    }
  } catch { /* ignore */ }
  return out;
}
checkHardcoded();

const warns = findings.filter(f => f.level === 'WARN');
const blockers = findings.filter(f => f.level === 'HIGH');

function md() {
  const L = ['# i18n Parity Report', '', `Project: \`${project}\``, '',
    `## Locales found — ${locales.length || 0}`, ''];
  for (const loc of locales) L.push(`- ${loc}: \`${localeFiles[loc].replace(project + '/', '')}\``);
  L.push('', `## Findings — ${warns.length} warning(s)`, '');
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}`);
  L.push('', '## Notes', '',
    '- Parity is structural (keys). Translation quality needs human review.',
    '- Orphan keys are informational; missing keys should be filled before release.', '');
  return L.join('\n');
}

const out = args.json ? JSON.stringify({ project, locales, findings }, null, 2) : md();
if (args.output) writeOut(args.output, out); else console.log(out);
function writeOut(path, content) { import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8')); }
if (args.strict && (blockers.length > 0 || warns.length > 0)) process.exit(1);
