#!/usr/bin/env node
// validate-data-safety-readiness.mjs
// Detects SDKs/data-collection signals and produces a Data Safety review checklist.
// NEVER auto-fills the form. Suggests human review only.
// Flags: --project <path>  --output <path>  --strict  --json

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const detected = new Set();

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

// (dependency hint, source-code hint) -> Data Safety category + suggested disclosure
const SIGNALS = [
  { hint: /"@react-native-firebase\/auth"|\bfirebase\.auth\b|createUserWithEmailAndPassword/i, sdk: 'Firebase Auth', category: 'Personal info', suggest: 'Email, phone, or user ID (account creation / sign-in).' },
  { hint: /"@react-native-firebase\/firestore"|\bfirebase\.firestore\b|collection\(/i, sdk: 'Firestore', category: 'Personal info / User-generated content', suggest: 'User profile + user-generated content stored in Firestore.' },
  { hint: /"@react-native-firebase\/storage"|\bfirebase\.storage\b/i, sdk: 'Firebase Storage', category: 'Photos and videos / User-generated content', suggest: 'User-uploaded media (avatars, posts).' },
  { hint: /"@react-native-firebase\/(analytics|app-check)"|\bfirebase\.analytics\b|logEvent\(/i, sdk: 'Firebase Analytics', category: 'App activity / Diagnostics', suggest: 'App activity and diagnostics (analytics events).' },
  { hint: /"@react-native-firebase\/crashlytics"|\bcrashlytics\b|recordError\(/i, sdk: 'Crashlytics', category: 'Diagnostics', suggest: 'Crash logs and performance diagnostics.' },
  { hint: /react-native-purchases|revenuecat|Purchases\./i, sdk: 'RevenueCat', category: 'Purchase history / Financial info', suggest: 'Purchase history (entitlements, IAP ledger).' },
  { hint: /expo-notifications|@react-native-firebase\/messaging|\bpushNotification\b/i, sdk: 'Notifications', category: 'Device or other IDs', suggest: 'Push notification token (registration ID).' },
  { hint: /expo-location|@react-native-community\/geolocation|ACCESS_FINE_LOCATION/i, sdk: 'Location', category: 'Location', suggest: 'Approximate/precise location.' },
  { hint: /expo-camera|expo-image-picker.*CameraUsage|requestCameraPermissions/i, sdk: 'Camera', category: 'Photos and videos', suggest: 'Camera capture (photos/videos).' },
  { hint: /expo-image-picker|PhotoLibrary|photo-library/i, sdk: 'Photo library', category: 'Photos and videos', suggest: 'Photo library selection.' },
  { hint: /expo-contacts|Contacts\.|READ_CONTACTS/i, sdk: 'Contacts', category: 'Contacts', suggest: 'User contacts.' },
  { hint: /react-native-admob|@react-native-firebase\/admob|com\.google\.android\.gms\.ads|AD_ID/i, sdk: 'Ads / Advertising ID', category: 'Device or other IDs', suggest: 'Advertising ID.' },
];

function readText(p) {
  if (!existsSync(p)) return null;
  try { return readFileSync(p, 'utf8'); } catch { return null; }
}

function getDeps() {
  const pkg = readJson(join(project, 'package.json'));
  if (!pkg) return {};
  return { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}), ...(pkg.peerDependencies || {}) };
}
function readJson(p) { if (!existsSync(p)) return null; try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; } }

function scanCodeFiles() {
  const out = [];
  const roots = ['src', 'app', 'lib'];
  for (const r of roots) {
    const root = join(project, r);
    if (existsSync(root)) walk(root, out);
  }
  return out;
}
function walk(dir, out) {
  try {
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, e.name);
      if (e.isDirectory()) walk(full, out);
      else if (/\.(ts|tsx|js|jsx|kt|java|swift|m)$/i.test(e.name)) out.push(full);
    }
  } catch { /* ignore */ }
}

// detect
const deps = getDeps();
const depText = Object.keys(deps).join('\n');
const codeFiles = scanCodeFiles();
const codeBlob = codeFiles.map(f => readText(f) || '').join('\n');
const hay = depText + '\n' + codeBlob;

for (const s of SIGNALS) {
  if (s.hint.test(hay)) {
    detected.add(s.sdk);
    add('INFO', 'SDK_DETECTED', `Detected ${s.sdk}. Data Safety category to review: ${s.category}. Suggested disclosure: ${s.suggest}`, null);
  }
}

// privacy docs present?
const privacyFiles = ['PRIVACY.md', 'PRIVACY_POLICY.md', 'docs/privacy.md', 'docs/privacy-policy.md', 'privacy.md', 'privacy-policy.html'];
const hasPrivacy = privacyFiles.some(p => existsSync(join(project, p)));
if (!hasPrivacy) add('HIGH', 'NO_PRIVACY_POLICY', 'No privacy policy document detected. Google Play requires a live Privacy Policy URL.', null);
else add('INFO', 'PRIVACY_POLICY_FOUND', 'Privacy policy document detected. Ensure it is hosted and the URL is reachable.', null);

// account deletion?
const hasAccountDeletion = /deleteAccount|delete-account|accountDeletion|dataDeletion/i.test(hay);
if (detected.has('Firebase Auth') && !hasAccountDeletion) {
  add('HIGH', 'NO_ACCOUNT_DELETION', 'Firebase Auth detected but no account/data deletion flow found. Play requires in-app account deletion when accounts are offered.', null);
}

const blockers = findings.filter(f => f.level === 'HIGH');
const warns = findings.filter(f => f.level === 'WARN');

function md() {
  const L = ['# Data Safety Readiness Report', '',
    `Project: \`${project}\``, '',
    '> This report SUGGESTS categories to review. It does NOT fill the Data Safety Form. A human must confirm every declaration.', '',
    `## Detected signals — ${detected.size} SDK(s)/data type(s)`, ''];
  for (const s of [...detected]) L.push(`- ${s}`);
  L.push('', `## Findings — ${blockers.length} blocker(s), ${warns.length} warning(s)`, '');
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}`);
  L.push('', '## Human review required', '',
    '- Confirm each detected SDK maps to the correct Data Safety section.',
    '- Confirm "Data encrypted in transit" only if TLS is enforced end-to-end.',
    '- Confirm "Data deletion" / "Account deletion" declarations match app behavior.',
    '- Never reduce a declaration without technical evidence.', '');
  return L.join('\n');
}

const out = args.json ? JSON.stringify({ project, detected: [...detected], findings }, null, 2) : md();
if (args.output) writeOut(args.output, out); else console.log(out);
function writeOut(path, content) { import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8')); }
if (args.strict && (blockers.length > 0 || warns.length > 0)) process.exit(1);
