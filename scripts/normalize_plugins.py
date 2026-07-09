import json
import os
import glob

REPO_ROOT = "/Users/andersonlimadev/Projects/IA/lemon-ai-hub"
plugin_jsons = glob.glob(os.path.join(REPO_ROOT, "plugins", "*", "plugin.json"))

standard_author = {
    "name": "Anderson Lima",
    "url": "https://andersonlimahw.github.io"
}

for pjson_path in plugin_jsons:
    with open(pjson_path, 'r') as f:
        data = json.load(f)
        
    modified = False
    
    if data.get("author") != standard_author:
        data["author"] = standard_author
        modified = True
        
    if "license" not in data or data["license"] != "MIT":
        data["license"] = "MIT"
        modified = True
        
    if "keywords" not in data:
        data["keywords"] = ["skill", "lemon-ai-hub"]
        modified = True
    else:
        if "lemon-ai-hub" not in data["keywords"]:
            data["keywords"].insert(0, "lemon-ai-hub")
            modified = True
        if "skill" not in data["keywords"]:
            data["keywords"].insert(0, "skill")
            modified = True
            
    if modified:
        with open(pjson_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Normalized {pjson_path}")
