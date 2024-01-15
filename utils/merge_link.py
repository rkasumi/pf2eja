import json
import re

outpath = "./output.json"
json_c = None
json_l = None
with open("../compendium/pf2e.feats-srd.json", "r") as fh:
  json_c = json.load(fh)
with open("./feats-legacy.json", "r") as fh:
  json_l = json.load(fh)

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
        
        for u in uniq.keys():
            if u not in json_c['entries'][key]['description']:
                json_c['entries'][key]['description'] += '<p>'+u+'</p>'

with open(outpath, 'w', encoding='utf-8') as fh:
    json.dump(json_c, fh, indent=2, ensure_ascii=False)
