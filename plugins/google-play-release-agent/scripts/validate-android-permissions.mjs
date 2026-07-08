#!/usr/bin/env node
// validate-android-permissions.mjs
// Audits Android permissions from AndroidManifest.xml + Expo app config.
// Flags: --project <path>  --output <path>  --strict  --json

import { readFileSync, existsSync } from 'node:fs';
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

const SENSITIVE = {
  CAMERA: 'Camera capture — justify in Play Console; runtime permission UX required.',
  RECORD_AUDIO: 'Microphone — justify; high scrutiny.',
  READ_MEDIA_IMAGES: 'Photo access (Android 13+) — use Photo Picker if possible.',
  READ_MEDIA_VIDEO: 'Video access (Android 13+) — use Photo Picker if possible.',
  ACCESS_FINE_LOCATION: 'Precise location — justify; foreground use only unless declared.',
  ACCESS_COARSE_LOCATION: 'Approximate location — justify.',
  ACCESS_BACKGROUND_LOCATION: 'Background location — HIGH scrutiny; usually rejected without strong justification.',
  READ_CONTACTS: 'Contacts — high scrutiny; avoid unless core feature.',
  POST_NOTIFICATIONS: 'Notifications (Android 13+) — runtime permission UX required.',
  AD_ID: 'Advertising ID — declare in Data Safety; required only if ads SDK present.',
  QUERY_ALL_PACKAGES: 'Queries all packages — HIGH scrutiny; Play requires approved use case.',
  MANAGE_EXTERNAL_STORAGE: 'Broad storage — HIGH scrutiny; almost always rejected; use Scoped Storage.',
  READ_EXTERNAL_STORAGE: 'Legacy storage — deprecated Android 13+; migrate to scoped media.',
  WRITE_EXTERNAL_STORAGE: 'Legacy storage — deprecated; remove.',
  READ_PHONE_STATE: 'Phone state — high scrutiny; avoid.',
  SEND_SMS: 'SMS — high scrutiny; PAY policy applies.',
  READ_SMS: 'SMS — almost always rejected.',
};

function readText(p) { if (!existsSync(p)) return null; try { return readFileSync(p, 'utf8'); } catch { return null; } }
function readJson(p) { if (!existsSync(p)) return null; try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; } }

const declared = new Set();

// AndroidManifest.xml (native plugin / ejected project)
const manifestPaths = [
  join(project, 'android', 'app', 'src', 'main', 'AndroidManifest.xml'),
  join(project, 'AndroidManifest.xml'),
];
for (const m of manifestPaths) {
  const txt = readText(m);
  if (!txt) continue;
  const re = /android:name="android\.permission\.([A-Z_]+)"/g;
  let match;
  while ((match = re.exec(txt)) !== null) declared.add(match[1]);
}

// Expo app config (android.permissions + ios unused)
const appJson = readJson(join(project, 'app.json'));
const expoPerms = appJson?.expo?.android?.permissions;
if (Array.isArray(expoPerms)) {
  for (const p of expoPerms) {
    const clean = String(p).replace(/^android\.permission\./, '').toUpperCase();
    declared.add(clean);
  }
}

// analyze
if (declared.size === 0) {
  add('INFO', 'NO_PERMISSIONS_FOUND', 'No Android permissions found in manifest or app.json. Fine if the app needs none.', null);
}

for (const perm of declared) {
  if (SENSITIVE[perm]) {
    const level = /HIGH|almost always|background|QUERY_ALL_PACKAGES|MANAGE_EXTERNAL_STORAGE|SEND_SMS|READ_SMS/.test(SENSITIVE[perm]) ? 'HIGH' : 'WARN';
    add(level, 'SENSITIVE_PERMISSION', `${perm}: ${SENSITIVE[perm]}`, null);
  } else {
    add('INFO', 'PERMISSION_DECLARED', `${perm} declared (not in sensitive list).`, null);
  }
}

const blockers = findings.filter(f => f.level === 'HIGH');
const warns = findings.filter(f => f.level === 'WARN');

function md() {
  const L = ['# Android Permissions Report', '', `Project: \`${project}\``, '',
    `## Declared permissions — ${declared.size}`, ''];
  for (const p of [...declared].sort()) L.push(`- \`${p}\``);
  L.push('', `## Findings — ${blockers.length} blocker(s), ${warns.length} warning(s)`, '');
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}`);
  L.push('', '## Notes', '',
    '- "Unused" detection is heuristic — confirm each permission maps to real usage.',
    '- Provide runtime permission UX for CAMERA, LOCATION, NOTIFICATIONS, etc.',
    '- Remove deprecated/legacy permissions before release.', '');
  return L.join('\n');
}

const out = args.json ? JSON.stringify({ project, declared: [...declared].sort(), findings }, null, 2) : md();
if (args.output) writeOut(args.output, out); else console.log(out);
function writeOut(path, content) { import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8')); }
if (args.strict && (blockers.length > 0 || warns.length > 0)) process.exit(1);
