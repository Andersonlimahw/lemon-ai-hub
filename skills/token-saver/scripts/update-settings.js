#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const SETTINGS_PATH = path.join(process.env.HOME, '.claude', 'settings.json');
const BACKUP_PATH = SETTINGS_PATH + '.bak';

// Load settings
if (!fs.existsSync(SETTINGS_PATH)) {
  console.error(`Error: settings.json not found at ${SETTINGS_PATH}`);
  process.exit(1);
}

const settingsRaw = fs.readFileSync(SETTINGS_PATH, 'utf8');
let settings;
try {
  settings = JSON.parse(settingsRaw);
} catch (e) {
  console.error(`Error parsing settings.json: ${e.message}`);
  process.exit(1);
}

// Backup
fs.writeFileSync(BACKUP_PATH, settingsRaw, 'utf8');
console.log(`Backed up settings to ${BACKUP_PATH}`);

const enableRtk = process.env.ENABLE_RTK === '1';
const enableCaveman = process.env.ENABLE_CAVEMAN === '1';
const enableContextMode = process.env.ENABLE_CONTEXT_MODE === '1';

// Initialize structures if missing
settings.hooks = settings.hooks || {};
settings.enabledPlugins = settings.enabledPlugins || {};
settings.extraKnownMarketplaces = settings.extraKnownMarketplaces || {};

// Configure RTK
if (enableRtk) {
  settings.hooks.PreToolUse = settings.hooks.PreToolUse || [];
  
  // Check if rtk hook already exists
  const hasRtkHook = settings.hooks.PreToolUse.some(hookGroup => 
    hookGroup.matcher === 'Bash' && 
    hookGroup.hooks && 
    hookGroup.hooks.some(h => h.command && h.command.includes('rtk hook'))
  );

  if (!hasRtkHook) {
    settings.hooks.PreToolUse.push({
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "rtk hook claude"
        }
      ]
    });
    console.log("Added RTK bash hook to PreToolUse");
  } else {
    console.log("RTK bash hook already present");
  }
}

// Configure Caveman
if (enableCaveman) {
  settings.enabledPlugins["caveman@caveman"] = true;
  settings.extraKnownMarketplaces["caveman"] = {
    "source": {
      "source": "github",
      "repo": "JuliusBrussee/caveman"
    }
  };
  console.log("Enabled Caveman plugin and added to extraKnownMarketplaces");
}

// Configure Context-Mode
if (enableContextMode) {
  settings.enabledPlugins["context-mode@context-mode"] = true;
  settings.extraKnownMarketplaces["context-mode"] = {
    "source": {
      "source": "github",
      "repo": "mksglu/context-mode"
    }
  };
  console.log("Enabled Context-Mode plugin and added to extraKnownMarketplaces");
}

// Write settings back
fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings, null, 2), 'utf8');
console.log("Updated settings.json successfully!");
