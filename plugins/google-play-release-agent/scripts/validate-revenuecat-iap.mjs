#!/usr/bin/env node
// validate-revenuecat-iap.mjs
// RevenueCat / IAP Android readiness audit (static).
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

function readText(p) { if (!existsSync(p)) return null; try { return readFileSync(p, 'utf8'); } catch { return null; } }

// gather code blob (src/app/lib) + env example files
function codeBlob() {
  const out = [];
  for (const r of ['src', 'app', 'lib']) { const root = join(project, r); if (existsSync(root)) walk(root, out); }
  return out.map(f => ({ f, t: readText(f) || '' }));
}
function walk(dir, out) {
  try { for (const e of readdirSync(dir, { withFileTypes: true })) { const full = join(dir, e.name); if (e.isDirectory()) walk(full, out); else if (/\.(ts|tsx|js|jsx)$/i.test(e.name)) out.push(full); } } catch { /* ignore */ }
}

const blob = codeBlob();
const hay = blob.map(b => b.t).join('\n');

// 1. public RC keys
const envFiles = ['.env', '.env.example', '.env.local', '.env.production', 'app.config.js', 'app.config.ts', 'app.json'];
let androidKeySeen = false;
for (const ef of envFiles) {
  const txt = readText(join(project, ef));
  if (!txt) continue;
  if (/EXPO_PUBLIC_RC_ANDROID_KEY\s*=/.test(txt)) { androidKeySeen = true; add('INFO', 'RC_ANDROID_KEY_REF', 'EXPO_PUBLIC_RC_ANDROID_KEY referenced in ' + ef, ef); }
  if (/EXPO_PUBLIC_RC_IOS_KEY\s*=/.test(txt)) add('INFO', 'RC_IOS_KEY_REF', 'EXPO_PUBLIC_RC_IOS_KEY referenced (cross-platform hint) in ' + ef, ef);
}
if (!androidKeySeen) add('WARN', 'NO_RC_ANDROID_KEY', 'EXPO_PUBLIC_RC_ANDROID_KEY not found. RevenueCat Android purchases require a public Android SDK key.', null);

// 2. RC SDK present?
if (!/react-native-purchases|@revenuecat|Purchases\./.test(hay)) {
  add('WARN', 'NO_RC_SDK', 'No react-native-purchases / RevenueCat SDK usage detected.', null);
}

// 3. products referenced in code (heuristic)
const productIds = new Set();
const prodRe = /(?:productId|product_id|sku|offeringIdentifier|packageIdentifier|entitlement)\s*[:=]\s*['"`]([a-z0-9_.-]+)['"`]/gi;
let m;
while ((m = prodRe.exec(hay)) !== null) productIds.add(m[1]);

// 4. store metadata file (entitlements/products)?
const metaCandidates = ['revenuecat.json', 'rc-products.json', 'products.json', 'entitlements.json', 'metadata/revenuecat.json'];
const metaProducts = new Set();
for (const mc of metaCandidates) {
  const p = join(project, mc);
  const txt = readText(p);
  if (!txt) continue;
  const re = /"([a-z0-9_.-]+)"/gi;
  let mm;
  while ((mm = re.exec(txt)) !== null) metaProducts.add(mm[1]);
}

for (const id of productIds) {
  if (metaProducts.size && !metaProducts.has(id)) {
    add('WARN', 'PRODUCT_NO_METADATA', `Product/entitlement "${id}" referenced in code but not found in detected metadata file.`, null);
  } else {
    add('INFO', 'PRODUCT_REF', `Product/entitlement referenced in code: "${id}"`, null);
  }
}

// 5. restore purchases
if (!/restorePurchases|restore_purchases|restore-purchases/i.test(hay)) {
  add('HIGH', 'NO_RESTORE_PURCHASES', 'No restorePurchases call detected. Google Play requires a restore mechanism for IAP.', null);
}

// 6. paywall fallback
if (!/fallback|paywallFallback|defaultPaywall|catchAll/i.test(hay)) {
  add('WARN', 'NO_PAYWALL_FALLBACK', 'No obvious paywall fallback. Ensure users see a default paywall if RC offering fails to load.', null);
}

// 7. risky paywall wording
const RISKY = [/apost/i, /betting/i, /ganhe\s+dinheiro/i, /saque\s+garantido/i, /lucro/i, /cashout/i];
for (const r of RISKY) {
  if (r.test(hay)) add('HIGH', 'PAYWALL_RISKY_WORDING', `Risky wording (${r.source}) detected near paywall/IAP code. Use neutral wording (virtual currency, no payout).`, null);
}

const blockers = findings.filter(f => f.level === 'HIGH');
const warns = findings.filter(f => f.level === 'WARN');

function md() {
  const L = ['# RevenueCat / IAP Android Report', '', `Project: \`${project}\``, '',
    `## Products referenced — ${productIds.size}`, ''];
  for (const id of [...productIds]) L.push(`- \`${id}\``);
  L.push('', `## Findings — ${blockers.length} blocker(s), ${warns.length} warning(s)`, '');
  for (const f of findings) L.push(`- [${f.level}] **${f.code}** — ${f.message}${f.file ? ` (\`${f.file}\`)` : ''}`);
  L.push('', '## Notes', '',
    '- Confirm every product ID exists in Play Console with matching base plan + offer.',
    '- Ensure the Play Console service account is connected to RevenueCat.',
    '- Test a sandbox purchase before submission.', '');
  return L.join('\n');
}

const out = args.json ? JSON.stringify({ project, productIds: [...productIds], findings }, null, 2) : md();
if (args.output) writeOut(args.output, out); else console.log(out);
function writeOut(path, content) { import('node:fs').then(({ writeFileSync }) => writeFileSync(resolve(path), content + '\n', 'utf8')); }
if (args.strict && (blockers.length > 0 || warns.length > 0)) process.exit(1);
