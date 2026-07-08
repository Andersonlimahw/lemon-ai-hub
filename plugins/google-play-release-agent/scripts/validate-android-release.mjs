#!/usr/bin/env node
// validate-android-release.mjs
// Build readiness audit for an Expo/React Native Android release.
// Flags: --project <path>  --output <path>  --strict  --json
// Static-only. Reads filesystem + regex. Never builds or publishes.

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, resolve, extname } from 'node:path';

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const metrics = {};

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

function add(level, code, message, file = null) {
  findings.push({ level, code, message, file });
}

function readJson(path) {
  if (!existsSync(path)) return null;
  try { return JSON.parse(readFileSync(path, 'utf8')); } catch { return null; }
}

function readFile(path) {
  if (!existsSync(path)) return null;
  try { return readFileSync(path, 'utf8'); } catch { return null; }
}

// --- resolve expo config ----------------------------------------------------
function resolveExpoConfig() {
  const appJsonPath = join(project, 'app.json');
  const appConfigJs = join(project, 'app.config.js');
  const appConfigTs = join(project, 'app.config.ts');
  if (existsSync(appJsonPath)) {
    const data = readJson(appJsonPath);
    return { source: 'app.json', expo: data?.expo || data || {}, raw: data };
  }
  for (const p of [appConfigJs, appConfigTs]) {
    if (existsSync(p)) return { source: p.replace(project + '/', ''), expo: null, raw: null, isDynamic: true };
  }
  return null;
}

// --- checks -----------------------------------------------------------------
function checkExpoConfig(cfg) {
  if (!cfg) { add('ERROR', 'NO_EXPO_CONFIG', 'No app.json or app.config.* found (not an Expo project?).', null); return; }
  metrics.configSource = cfg.source;
  if (cfg.isDynamic) {
    add('INFO', 'DYNAMIC_CONFIG', `Dynamic config detected (${cfg.source}); static checks skipped on expo fields. Open the file and verify android.* manually.`, cfg.source);
    return;
  }
  const expo = cfg.expo || {};
  if (!expo.name) add('WARN', 'NO_APP_NAME', 'expo.name missing.', cfg.source);
  if (!expo.version) add('WARN', 'NO_VERSION', 'expo.version missing.', cfg.source);
  else metrics.appVersion = expo.version;
  const android = expo.android || {};
  if (!android.package) add('ERROR', 'NO_PACKAGE', 'android.package missing (required for Play Store).', cfg.source);
  else {
    metrics.package = android.package;
    if (!/^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$/i.test(android.package)) {
      add('WARN', 'BAD_PACKAGE_FORMAT', `android.package "${android.package}" may not match reverse-DNS format.`, cfg.source);
    }
  }
  if (android.versionCode == null) add('ERROR', 'NO_VERSION_CODE', 'android.versionCode missing (must be a positive integer, incremented per release).', cfg.source);
  else {
    metrics.versionCode = android.versionCode;
    if (!Number.isInteger(android.versionCode) || android.versionCode < 1) add('ERROR', 'BAD_VERSION_CODE', `android.versionCode must be a positive integer (got ${android.versionCode}).`, cfg.source);
  }
  if (android.versionCode != null && !expo.version) add('WARN', 'NO_VERSION_NAME', 'Consider setting expo.version as the user-facing versionName.', cfg.source);
  return android;
}

function checkEasJson() {
  const easPath = join(project, 'eas.json');
  if (!existsSync(easPath)) { add('WARN', 'NO_EAS_JSON', 'eas.json missing. EAS Build/Submit not configured.', null); return null; }
  const eas = readJson(easPath);
  if (!eas) { add('WARN', 'EAS_JSON_INVALID', 'eas.json is not valid JSON.', easPath); return null; }
  metrics.easJson = true;
  const build = eas.build || {};
  const production = build.production;
  if (!production) { add('WARN', 'NO_PRODUCTION_PROFILE', 'eas.json has no build.production profile.', easPath); return eas; }
  metrics.productionProfile = true;
  const androidEnv = production.android || {};
  const env = production.env || {};
  if (env.EXPO_PUBLIC_USE_MOCK === 'true' || androidEnv.EXPO_PUBLIC_USE_MOCK === 'true') {
    add('ERROR', 'MOCK_ON_IN_PRODUCTION', 'EXPO_PUBLIC_USE_MOCK=true detected in eas.json production profile. Release build MUST NOT use mock data.', easPath);
  }
  return eas;
}

function checkMockFlag() {
  // Heuristic: grep common env files for mock-on (only flag presence, never print contents)
  const candidates = ['.env.production', '.env', 'app.config.js', 'app.config.ts', 'app.json'];
  for (const c of candidates) {
    const p = join(project, c);
    const txt = readFile(p);
    if (!txt) continue;
    if (/EXPO_PUBLIC_USE_MOCK\s*=\s*['"]?true/i.test(txt) && !/production/i.test(c) === false ? /EXPO_PUBLIC_USE_MOCK\s*=\s*['"]?true/i.test(txt) : false) {
      // avoid false positives on .env.example etc.
      if (!/example/i.test(c)) add('WARN', 'MOCK_FLAG_PRESENT', `EXPO_PUBLIC_USE_MOCK=true found in ${c}. Confirm it is OFF for release.`, c);
    }
  }
}

function checkQualityGates() {
  const pkg = readJson(join(project, 'package.json'));
  if (!pkg) { add('WARN', 'NO_PACKAGE_JSON', 'No package.json found.', null); return; }
  const scripts = pkg.scripts || {};
  const want = ['lint', 'test', 'typecheck', 'tsc'];
  const present = want.filter(s => scripts[s]);
  metrics.qualityGates = present;
  const missing = want.filter(s => !scripts[s]);
  if (missing.length) add('INFO', 'QUALITY_GATE_MISSING', `Missing suggested scripts: ${missing.join(', ')}.`, 'package.json');
}

function checkBuildOutput() {
  // EAS produces .aab on cloud; local fastlane/dir build may produce apk. Flag apks in repo as potential confusion.
  const androidDir = join(project, 'android');
  if (!existsSync(androidDir)) return;
  const gradle = join(androidDir, 'app', 'build.gradle');
  if (existsSync(gradle)) {
    const txt = readFile(gradle);
    if (txt && /\babic\s*=\s*true\b|\bbundle\b|release\.[A-Za-z]+\.apk/i.test(txt)) {
      // can't reliably infer aab vs apk from text; just note native android present
      metrics.nativeAndroid = true;
    }
  }
}

function checkServiceAccountHint() {
  // Play Submit needs a service account key. Only check that eas submit references it; never read its contents.
  const eas = readJson(join(project, 'eas.json'));
  const submit = eas?.submit?.production?.android;
  if (submit && (submit.serviceAccountKeyPath || submit.serviceAccountKey)) {
    metrics.serviceAccountConfigured = true;
    add('INFO', 'SERVICE_ACCOUNT_REFERENCED', 'eas.json submit references a Play service account key. Confirm the file exists and is gitignored.', 'eas.json');
  } else {
    add('INFO', 'NO_SERVICE_ACCOUNT_HINT', 'No Play service account key referenced in eas.json submit. EAS Submit will need one.', null);
  }
}

// --- run --------------------------------------------------------------------
const cfg = resolveExpoConfig();
checkExpoConfig(cfg);
const eas = checkEasJson();
checkMockFlag();
checkQualityGates();
checkBuildOutput();
checkServiceAccountHint();

const errors = findings.filter(f => f.level === 'ERROR');
const warns = findings.filter(f => f.level === 'WARN');
const strictFail = args.strict && (errors.length > 0 || warns.length > 0);

// --- output -----------------------------------------------------------------
function mdReport() {
  const lines = [];
  lines.push('# Android Release Readiness Report');
  lines.push('');
  lines.push(`Project: \`${project}\``);
  lines.push(`Config source: ${metrics.configSource || 'n/a'}`);
  if (metrics.package) lines.push(`Package: \`${metrics.package}\``);
  if (metrics.versionCode != null) lines.push(`versionCode: ${metrics.versionCode}`);
  if (metrics.appVersion) lines.push(`versionName: ${metrics.appVersion}`);
  lines.push('');
  lines.push(`## Summary — ${errors.length} error(s), ${warns.length} warning(s)`);
  lines.push('');
  for (const f of findings) {
    lines.push(`- [${f.level}] **${f.code}** — ${f.message}${f.file ? ` (\`${f.file}\`)` : ''}`);
  }
  lines.push('');
  lines.push('## Verdict');
  if (errors.length > 0) lines.push('**NO_GO** — blocking errors present. Resolve before submission.');
  else if (warns.length > 0) lines.push('**GO_WITH_WARNINGS** — review each warning.');
  else lines.push('**GO** — build readiness checks passed.');
  return lines.join('\n');
}

if (args.json) {
  const payload = { project, metrics, findings, verdict: errors.length ? 'NO_GO' : (warns.length ? 'GO_WITH_WARNINGS' : 'GO') };
  const out = JSON.stringify(payload, null, 2);
  if (args.output) { writeOut(args.output, out); } else { console.log(out); }
} else {
  const md = mdReport();
  if (args.output) { writeOut(args.output, md); } else { console.log(md); }
}

function writeOut(path, content) {
  import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8'));
}

if (strictFail) process.exit(1);
