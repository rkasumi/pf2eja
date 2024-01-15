import json
import plyvel
import re

legacyName = "equipment"
compendiumName = "pf2e.equipment-srd.json"

#pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"
pathLegacy = "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/"
pathCompendium = "../compendium/"

json_l = {}
ldb = plyvel.DB(pathLegacy+legacyName, create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  json_l[j['name']] = j
ldb.close()

json_c = None
with open(pathCompendium+compendiumName, "r") as fh:
  json_c = json.load(fh)

for key in json_c['entries'].keys():
    if key in json_l:
        desc = json_l[key]['system']['description']['value']
        uniq = {}
        for m in re.finditer(r'(@UUID\[Compendium\.pf2e\..*?\])', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        for m in re.finditer(r'(@Damage\[.*?\])[\s\.]', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        for m in re.finditer(r'(@Check\[.*?\])[\s\.]', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        for m in re.finditer(r'(@Template\[.*?\])[\s\.]', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        for m in re.finditer(r'(\[\[/.*?\])[\s\.]', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        for m in re.finditer(r'(\[\[/.*?\]\]\])', desc, re.MULTILINE):
            uniq[m.groups()[0]] = 1
        
        for u in uniq.keys():
            if 'description' not in json_c['entries'][key]:
                continue
            if u not in json_c['entries'][key]['description']:
                json_c['entries'][key]['description'] += '<p>'+u+'</p>'

with open("./out-"+compendiumName, 'w', encoding='utf-8') as fh:
    json.dump(json_c, fh, indent=2, ensure_ascii=False)
