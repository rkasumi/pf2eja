import json
import plyvel
import shutil
import re
import os
pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"

json_c = None
with open("../../compendium/pf2e.feats-srd.json", "r") as fh:
  json_c = json.load(fh)

pathCompendium = "../../compendium/"
trans_list = [
  ('classfeatures', 'pf2e.classfeatures.json',),
  ('feats-srd', 'pf2e.feats-srd.json',),
]
translate = {}
for t in trans_list:
  with open(pathCompendium+t[1], "r") as fh:
    j = json.load(fh)
  for key in j['entries']:
    translate[key.lower()] = j['entries'][key]['name']

with open("mydata.json", "r") as fh:
  j = json.load(fh)
  for key in j.keys():
    translate[key.lower()] = j[key]

skill_list = [
  ("〈秘術〉", "arcana"),
  ("〈軽業〉", "acrobatics"),
  ("〈運動〉", "athletics"),
  ("〈製作〉", "crafting"),
  ("〈ペテン〉", "deception"),
  ("〈交渉〉", "diplomacy"),
  ("〈威圧〉", "intimidation"),
  ("〈知識〉", "lore"),
  ("〈医術〉", "medicine"),
  ("〈自然〉", "nature"),
  ("〈伝承学〉", "occultism"),
  ("〈芸能〉", "performance"),
  ("〈宗教〉", "religion"),
  ("〈社会〉", "society"),
  ("〈生存〉", "survival"),
  ("〈盗賊〉", "thievery"),
  ("〈隠密〉", "stealth"),
  ("〈知覚〉", "perception"),
]
for s in skill_list:
  translate["trained in "+s[1]] = s[0]+"の修得"
  translate["expert in "+s[1]] = s[0]+"の熟練"
  translate["master in "+s[1]] = s[0]+"の達人"
  translate["legendary in "+s[1]] = s[0]+"の伝説"

make_list = {}

ldb = plyvel.DB(pathLegacy+"feats-legacy", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  if j['name'] in json_c['entries']:
    jpj = json_c['entries'][j['name']]
    if len(jpj['name']) != len(jpj['name'].encode('utf-8')): # 日本語化済のもののみ対象
      json_c['entries'][j['name']]["prerequisites"] = []
      for p in j['system']['prerequisites']['value']:
        if p["value"].lower() in translate:
          json_c['entries'][j['name']]["prerequisites"].append({"value": translate[p["value"].lower()]})
        else:
          make_list[p["value"].lower()] = jpj['name']
          pass
ldb.close()

for u in make_list.keys():
    print(u)
    print(make_list[u])

with open("./pf2e.feats-srd.json", 'w', encoding='utf-8') as fh:
  json.dump(json_c, fh, indent=2, ensure_ascii=False)

 #8513       "prerequisites": [
 #8514         {"value": "交渉の伝説"}
 #8515       ],
