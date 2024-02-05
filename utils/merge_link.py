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
  { # 装備品
      "path": "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/",
      "legacyName": "equipment",
      "compendiumName": "pf2e.equipment-srd.json",
  },
]

trans_list = [
  ('actionspf2e', 'pf2e.actionspf2e.json',),
  ('ancestryfeatures', 'pf2e.ancestryfeatures.json',),
  ('backgrounds', 'pf2e.backgrounds.json',),
  ('bestiary-ability-glossary-srd', 'pf2e.bestiary-ability-glossary-srd.json',),
  ('classfeatures', 'pf2e.classfeatures.json',),
  ('conditionitems', 'pf2e.conditionitems.json',),
  ('equipment-srd', 'pf2e.equipment-srd.json',),
  ('familiar-abilities', 'pf2e.familiar-abilities.json',),
  ('feats-srd', 'pf2e.feats-srd.json',),
  ('heritages', 'pf2e.heritages.json',),
  ('pathfinder-bestiary', 'pf2e.pathfinder-bestiary.json',),
  ('pathfinder-bestiary-2', 'pf2e.pathfinder-bestiary-2.json',),
  ('pf2e.spells-srd', 'pf2e.spells-srd.json',),
]

pathCompendium = "../compendium/"


def merge_link(t, translate):
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
          for m in re.finditer(r'(@UUID\[Compendium\.pf2e\..*?\]){(.*?)}', desc, re.MULTILINE):
              uniq[m.groups()[0]] = m.groups()[1]
          for u in uniq.keys():
              if 'description' not in json_c['entries'][key]:
                  continue
              json_c['entries'][key]['description'] = json_c['entries'][key]['description'].replace("<p>"+u+"</p>", "")
              if u not in json_c['entries'][key]['description']:
                  if uniq[u] in translate:
                      json_c['entries'][key]['description'] = \
                        json_c['entries'][key]['description'].replace(translate[uniq[u]], u+"{"+translate[uniq[u]]+"}")
                  else:
                    json_c['entries'][key]['description'] += '<p>'+u+'</p>'

          uniq = {}
          for m in re.finditer(r'(@Damage\[.*?\])[a-z;\s\.{\),]', desc, re.MULTILINE):
              uniq[m.groups()[0]] = 1
          for m in re.finditer(r'(@Check\[.*?\])[a-z;\s\.{\),]', desc, re.MULTILINE):
              uniq[m.groups()[0]] = 1
          for m in re.finditer(r'(@Template\[.*?\])[a-z;\s\.{\),]', desc, re.MULTILINE):
              uniq[m.groups()[0]] = 1
          for m in re.finditer(r'(\[\[/.*?\])[a-z;\s\.{\),]', desc, re.MULTILINE):
              uniq[m.groups()[0]] = 1
          for m in re.finditer(r'(\[\[/.*?\]\]\])', desc, re.MULTILINE):
              uniq[m.groups()[0]] = 1
          
          for u in uniq.keys():
              if 'description' not in json_c['entries'][key]:
                  continue
              json_c['entries'][key]['description'] = json_c['entries'][key]['description'].replace("<p>"+u+"</p>", "")
              if u not in json_c['entries'][key]['description']:
                  json_c['entries'][key]['description'] += '<p>'+u+'</p>'
  
  with open("./"+t["compendiumName"], 'w', encoding='utf-8') as fh:
      json.dump(json_c, fh, indent=2, ensure_ascii=False)

translate = {}
for t in trans_list:
  with open(pathCompendium+t[1], "r") as fh:
    j = json.load(fh)
  for key in j['entries']:
    translate[key] = j['entries'][key]['name']

translate["Bag of Holding"] = "バッグ・オヴ・ホールディング"
translate["Bag of Holding (Type I)"] = "タイプIのバッグ・オヴ・ホールディング"
translate["Bag of Holding (Type II)"] = "タイプIIのバッグ・オヴ・ホールディング"
translate["Tanglefoot Bags"] = "足留め袋"
translate["Clumsy 1"] = "よたつき状態1"
translate["Clumsy 2"] = "よたつき状態2"
translate["Clumsy 3"] = "よたつき状態3"
translate["Doomed 1"] = "凶兆状態1"
translate["Doomed 2"] = "凶兆状態1"
translate["Drained 1"] = "吸精状態1"
translate["Drained 2"] = "吸精状態2"
translate["Drained 3"] = "吸精状態3"
translate["Drained 4"] = "吸精状態4"
translate["Dying 1"] = "瀕死状態1"
translate["Enfeebled 1"] = "虚弱状態"
translate["Enfeebled 2"] = "虚弱状態"
translate["Enfeebled 3"] = "虚弱状態"
translate["Enfeebled 4"] = "虚弱状態"
translate["Frightened 1"] = "恐れ状態1"
translate["Frightened 2"] = "恐れ状態2"
translate["Frightened 3"] = "恐れ状態3"
translate["Frightened 4"] = "恐れ状態4"
translate["Sickened 1"] = "不調状態"
translate["Sickened 2"] = "不調状態"
translate["Sickened 3"] = "不調状態"
translate["Sickened 4"] = "不調状態"
translate["Slowed 1"] = "減速状態1"
translate["Slowed 2"] = "減速状態2"
translate["Stunned 1"] = "朦朧状態"
translate["Stunned 2"] = "朦朧状態"
translate["Stunned 3"] = "朦朧状態"
translate["Stunned 4"] = "朦朧状態"
translate["Stupefied 1"] = "知性低下状態"
translate["Stupefied 2"] = "知性低下状態"
translate["Stupefied 3"] = "知性低下状態"
translate["Stupefied 4"] = "知性低下状態"
translate["Wounded 1"] = "重傷状態1"
translate["Wounded 2"] = "重傷状態2"

for t in target_list:
  merge_link(t, translate)
