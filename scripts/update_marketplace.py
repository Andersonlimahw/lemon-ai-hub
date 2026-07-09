import json
import os
import glob

REPO_ROOT = "/Users/andersonlimadev/Projects/IA/lemon-ai-hub"
MARKETPLACE_PATH = os.path.join(REPO_ROOT, ".claude-plugin/marketplace.json")
README_PATH = os.path.join(REPO_ROOT, "README.md")

with open(MARKETPLACE_PATH, 'r') as f:
    marketplace = json.load(f)

# Find all plugin.json
plugin_jsons = glob.glob(os.path.join(REPO_ROOT, "plugins", "*", "plugin.json"))

new_plugins = []
for pjson_path in plugin_jsons:
    with open(pjson_path, 'r') as f:
        data = json.load(f)
        
    plugin_name = data.get("name")
    if not plugin_name:
        plugin_name = os.path.basename(os.path.dirname(pjson_path))
        
    new_plugins.append({
        "name": plugin_name,
        "source": f"./plugins/{plugin_name}",
        "description": data.get("description", ""),
        "version": data.get("version", "1.0.0"),
        "license": data.get("license", "MIT"),
        "keywords": data.get("keywords", [])
    })

# Sort alphabetically by name
new_plugins = sorted(new_plugins, key=lambda x: x["name"])

marketplace["plugins"] = new_plugins

with open(MARKETPLACE_PATH, 'w') as f:
    json.dump(marketplace, f, indent=2)

print("Marketplace updated successfully.")

# Update README.md table
with open(README_PATH, 'r') as f:
    lines = f.readlines()

new_lines = []
in_table = False
table_inserted = False

for line in lines:
    if line.startswith('| `'):
        in_table = True
        continue
    if in_table and not line.startswith('|'):
        in_table = False
        
        # Insert the new table
        for plugin in new_plugins:
            name = plugin["name"]
            desc = plugin["description"].replace('\n', ' ')
            new_lines.append(f"| `{name}` | {desc} |\n")
        table_inserted = True
        
    new_lines.append(line)

with open(README_PATH, 'w') as f:
    f.writelines(new_lines)
    
print("README updated successfully.")
