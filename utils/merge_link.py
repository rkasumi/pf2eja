import json
import plyvel
import re

target_list = [
  { # 特技
      "path": "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/",
      "legacyName": "feats-legacy",
      "compendiumName": "pf2e.feats-srd.json",
  },
  { # クラス特徴
      "path": "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/",
      "legacyName": "class-features-legacy",
      "compendiumName": "pf2e.classfeatures.json",
  },
  { # 呪文
      "path": "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/",
      "legacyName": "spells-legacy",
      "compendiumName": "pf2e.spells-srd.json",
  },
  { # アクション
      "path": "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/",
      "legacyName": "actions-legacy",
      "compendiumName": "pf2e.actionspf2e.json",
  },
  #{ # 装備品
  #    "path": "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/",
  #    "legacyName": "equipment",
  #    "compendiumName": "pf2e.equipment-srd.json",
  #},
]

pathCompendium = "../compendium/"

def merge_link(t):
  json_l = {}
  ldb = plyvel.DB(t["path"]+t["legacyName"], create_if_missing=False)
  for key, line in ldb:
    j = json.loads(line)
    json_l[j['name']] = j
  ldb.close()
  
  json_c = None
  with open(pathCompendium+t["compendiumName"], "r") as fh:
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
  
  with open("./out-"+t["compendiumName"], 'w', encoding='utf-8') as fh:
      json.dump(json_c, fh, indent=2, ensure_ascii=False)

for t in target_list:
  merge_link(t)
