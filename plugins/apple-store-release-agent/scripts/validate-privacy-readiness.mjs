#!/usr/bin/env node
// validate-privacy-readiness.mjs — privacy policy/terms, SDK data-collection map, permission usage,
// suggested App Privacy labels (suggestion only — never auto-declare).
// Zero deps, ESM, Node >= 18. Flags: --project --output --strict --json
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const args = parseArgs(process.argv.slice(2));
const project = resolve(args.project || process.cwd());
const findings = [];
const add = (severity, area, message, file, line) =>
  findings.push({ severity, area, message, file, line });

const SKIP = /[\\/](node_modules|\.git|dist|build|coverage)[\\/]/;
const EXT = /\.(tsx|ts|jsx|js|mjs|json)$/;

// SDK -> Apple privacy data category (suggestion only)
const SDK_MAP = [
  { re: /@react-native-firebase\/auth|expo-firebase-auth|firebase\/auth|signInWithEmail/i, sdk: "Firebase Auth", categories: ["Contact Info (Email)", "Identifiers (User ID)"] },
  { re: /@react-native-firebase\/(firestore|storage)|expo-firebase-(firestore|storage)|cloud.firestore/i, sdk: "Firestore/Storage", categories: ["User Content (Photos or User Content)"] },
  { re: /@react-native-firebase\/analytics|expo-firebase-analytics|firebase\/analytics/i, sdk: "Firebase Analytics", categories: ["Usage Data (Product Interaction)", "Diagnostics"] },
  { re: /@react-native-firebase\/crashlytics|expo-firebase-crashlytics/i, sdk: "Crashlytics", categories: ["Diagnostics (Crash Data)"] },
  { re: /react-native-purchases|@revenuecat/i, sdk: "RevenueCat", categories: ["Purchases (Purchase History)"] },
  { re: /@react-native-firebase\/messaging|expo-notifications|pushNotification/i, sdk: "Notifications", categories: ["Identifiers (Device ID)"] },
  { re: /expo-location|Geolocation|requestForegroundPermissions.*location/i, sdk: "Location", categories: ["Location (Precise or Coarse)"] },
  { re: /expo-camera|expo-image-picker|RCTCamera/i, sdk: "Camera/Photos", categories: ["Photos or Videos"] },
];
const detected = new Map(); // sdk -> categories

let policyUrl = null;
let termsUrl = null;
let hasAtt = false;
let signupPresent = false;
let deleteAccount = false;
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
    const base = e.toLowerCase();
    if (/\.(md|txt|json|tsx|ts|jsx|js|mjs)$/.test(base) && scanned < 1500) {
      scanned++;
      let text = "";
      try { text = readFileSync(p, "utf8"); } catch { continue; }
      // urls
      if (!policyUrl) {
        const m = text.match(/https?:\/\/[^\s)"']+privacy[\w-./]*/i);
        if (m) policyUrl = m[0];
      }
      if (!termsUrl) {
        const m = text.match(/https?:\/\/[^\s)"']+(?:terms|tos|termos-de-uso)[\w-./]*/i);
        if (m) termsUrl = m[0];
      }
      // ATT
      if (/NSUserTrackingUsageDescription|AppTrackingTransparency|requestTrackingPermissions/i.test(text)) hasAtt = true;
      // signup / delete account
      if (/createUser|signUp|sign_up|register|sign-up|criar conta|cadastro/i.test(text)) signupPresent = true;
      if (/deleteAccount|delete-account|delete_account|excluir conta|eliminar cuenta/i.test(text)) deleteAccount = true;
      // SDKs
      for (const def of SDK_MAP) {
        if (def.re.test(text)) {
          if (!detected.has(def.sdk)) detected.set(def.sdk, new Set(def.categories));
          else def.categories.forEach((c) => detected.get(def.sdk).add(c));
        }
      }
    }
  }
}
walk(project);

// policy/terms required
if (!policyUrl) add("BLOCKER", "privacy", "No Privacy Policy URL found.", null);
if (!termsUrl) add("BLOCKER", "privacy", "No Terms of Service URL found.", null);

// account deletion required when signup exists
if (signupPresent && !deleteAccount) {
  add("BLOCKER", "privacy", "Signup detected but no in-app account deletion path found (App Store requires it).", null);
} else if (signupPresent && deleteAccount) {
  add("INFO", "privacy", "Signup + account deletion both detected.", null);
}

// ATT if any tracking-ish SDK
const trackingSdk = detected.has("Firebase Analytics") || detected.has("Notifications");
if (trackingSdk && !hasAtt) {
  add("WARNING", "privacy", "Analytics/notifications SDK detected but no ATT prompt found — confirm if tracking applies.", null);
}

// secrets hygiene (names only)
for (const f of ["GoogleService-Info.plist", "google-services.json"]) {
  const p = join(project, f);
  if (existsSync(p)) add("WARNING", "privacy", `${f} present — ensure gitignored, not committed.`, p);
}

// suggested labels (suggestion only)
const suggestedLabels = [...new Set([...detected.values()].flatMap((s) => [...s]))];

const decision = decide(findings);
const report = render(findings, decision, project, { policyUrl, termsUrl, hasAtt, signupPresent, deleteAccount, detected: [...detected.keys()], suggestedLabels });
if (args.output) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(resolve(args.output), report, "utf8");
} else if (!args.json) console.log(report);
if (args.json) console.log(JSON.stringify({ project, decision, findings, meta: { policyUrl, termsUrl, hasAtt, signupPresent, deleteAccount, detected: [...detected.keys()], suggestedLabels } }, null, 2));
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
  lines.push("# Privacy Readiness Audit");
  lines.push(`**Project:** ${project}`);
  lines.push(`**Decision:** ${decision}`);
  lines.push("");
  lines.push(`- Privacy Policy URL: ${meta.policyUrl || "(missing)"}`);
  lines.push(`- Terms URL: ${meta.termsUrl || "(missing)"}`);
  lines.push(`- ATT prompt: ${meta.hasAtt}`);
  lines.push(`- Signup: ${meta.signupPresent} | Account deletion: ${meta.deleteAccount}`);
  lines.push(`- Detected SDKs: ${meta.detected.length ? meta.detected.join(", ") : "(none)"}`);
  lines.push("");
  lines.push("**Suggested App Privacy labels (HUMAN MUST CONFIRM — suggestion only):**");
  if (meta.suggestedLabels.length) for (const l of meta.suggestedLabels) lines.push(`- ${l}`);
  else lines.push("- (no SDK data collection inferred)");
  lines.push("");
  lines.push("| Severity | Area | Message | File:Line |");
  lines.push("| --- | --- | --- | --- |");
  for (const f of list) lines.push(`| ${f.severity} | ${f.area} | ${f.message} | ${f.file || "-"}${f.line ? ":" + f.line : ""} |`);
  if (!list.length) lines.push("| (none) | - | No findings. | - |");
  return lines.join("\n");
}
