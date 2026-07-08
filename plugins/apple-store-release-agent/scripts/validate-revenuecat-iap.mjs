#!/usr/bin/env node
// validate-revenuecat-iap.mjs — RevenueCat/IAP static readiness (public envs, products, restore, paywall).
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

const SKIP = /[\\/](node_modules|\.git|dist|build|coverage)[\\/]/;
const EXT = /\.(tsx|ts|jsx|js|mjs)$/;

let hasRcSdk = false;
let hasIapRn = false;
const productIds = new Set();
let hasRestore = false;
let hasPaywall = false;
let hasFallback = false;
let scanned = 0;

function walk(dir) {
  let entries = [];
  try { entries = readdirSync(dir); } catch { return; }
  for (const e of entries) {
    if (e === "node_modules" || e === ".git" || e === "dist" || e === "build") continue;
    const p = join(dir, e);
    let st; try { st = statSync(p); } catch { continue; }
    if (SKIP.test(p)) continue;
    if (st.isDirectory()) { walk(p); continue; }
    if (!EXT.test(e) && !/\.env/.test(e)) continue;
    if (scanned > 1500) continue;
    scanned++;
    let text = "";
    try { text = readFileSync(p, "utf8"); } catch { continue; }
    if (/react-native-purchases|@revenuecat\/pod|Purchases\.(configure|getCustomerInfo|purchasePackage|getOfferings)/.test(text)) hasRcSdk = true;
    if (/react-native-iap|RNIap\.|requestPurchase|getProducts/.test(text)) hasIapRn = true;
    // restore heuristics
    if (/restorePurchases|Purchases\.restorePurchases|restorePurchase\b|RNIap\.(restore|restoreAll)/i.test(text)) hasRestore = true;
    // paywall
    if (/paywall|Paywall/i.test(text)) hasPaywall = true;
    // fallback hint when products fail (loose; deeper check out of MVP scope)
    if (/(catch|fallback|onError|errorBoundary|isLoading|entitlement)/i.test(text)) {} // noop marker
    // product ids: iOS convention <letters>_<words> e.g. com_app_pro_monthly
    const re = /["']([a-z0-9_.]{4,}_(?:pro|premium|monthly|yearly|annual|coins|pack|starter|plus|subscription)[a-z0-9_]*)["']/gi;
    let m;
    while ((m = re.exec(text))) productIds.add(m[1]);
  }
}
walk(project);

// public env detection (names only)
const PUBLIC_IOS = /EXPO_PUBLIC_RC_IOS_KEY\s*=\s*['"]?[\w]+/i;
const PUBLIC_ANDROID = /EXPO_PUBLIC_RC_ANDROID_KEY\s*=\s*['"]?[\w]+/i;
let iosKey = false;
for (const f of [".env", ".env.local", ".env.production", ".env.example"]) {
  const p = join(project, f);
  if (!existsSync(p)) continue;
  const t = readFileSync(p, "utf8");
  if (PUBLIC_IOS.test(t)) iosKey = true;
}
// also scan source for the literal (public key is safe to reference)
if (!iosKey) {
  // quick re-scan limited to non-env files already done; check a flag we set
  // (kept simple: rely on env detection + a source hint)
}

if (!hasRcSdk && !hasIapRn) {
  add(args.strict ? "WARNING" : "INFO", "iap", "No RevenueCat / react-native-iap usage detected; IAP audit skipped.", null);
} else {
  if (!iosKey) add("WARNING", "iap-env", "EXPO_PUBLIC_RC_IOS_KEY not found in env files (needed for RevenueCat iOS).", null);
  if (!hasRestore) add("BLOCKER", "iap-restore", "No restore-purchases path detected — required by App Review.", null);
  if (!hasPaywall) add("WARNING", "iap-paywall", "No paywall component detected.", null);
  // paywall fallback heuristic
  hasFallback = hasPaywall; // basic; deeper check out of scope for MVP
  if (productIds.size === 0) add("INFO", "iap-products", "No IAP product IDs inferred from code (naming heuristic).", null);
}

const decision = decide(findings);
const report = render(findings, decision, project, { hasRcSdk, hasIapRn, hasRestore, productIds: [...productIds] });
if (args.output) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(resolve(args.output), report, "utf8");
} else if (!args.json) console.log(report);
if (args.json) console.log(JSON.stringify({ project, decision, findings, meta: { hasRcSdk, hasIapRn, hasRestore, productIds: [...productIds] } }, null, 2));
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
function render(list, decision, project, meta) {
  const lines = [];
  lines.push("# RevenueCat / IAP Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push(`- RevenueCat SDK detected: ${meta.hasRcSdk}`);
  lines.push(`- react-native-iap detected: ${meta.hasIapRn}`);
  lines.push(`- Restore purchases path: ${meta.hasRestore}`);
  lines.push(`- Inferred product IDs: ${meta.productIds.length ? meta.productIds.join(", ") : "(none)"}`);
  lines.push("");
  lines.push("| Severity | Area | Message | File:Line |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"}${f.line ? ":" + f.line : ""} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
