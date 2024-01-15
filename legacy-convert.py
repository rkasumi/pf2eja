import json
import plyvel
import shutil
import re
import os
# 本PG実行後にfvtt再起動すること
path = "/home/yaginumad/userdata_pf/Data/systems/pf2e/"
pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"
pathRemaster = "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/"

# 呪文リストをコンバートする
#   旧： system.traditions.valueに体系(秘術、信仰、始原、伝承)が記録
#   新： syste.traits.traditionsに体系が記録
# 旧DBを新PGで使用するため、旧→新にデータコンバートする。
ldb = plyvel.DB(pathLegacy+"spells-legacy", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  if j["system"]["components"].get("somatic") and\
      "manipulate" not in j["system"]["traits"]["value"]:
      j["system"]["traits"]["value"].append("manipulate")
  if j["system"]["components"].get("material") and\
      "manipulate" not in j["system"]["traits"]["value"]:
      j["system"]["traits"]["value"].append("manipulate")
  if j["system"]["components"].get("focus") and\
      "manipulate" not in j["system"]["traits"]["value"]:
      j["system"]["traits"]["value"].append("manipulate")
  if j["system"]["components"].get("verbal") and\
      "concentrate" not in j["system"]["traits"]["value"]:
      j["system"]["traits"]["value"].append("concentrate")

  if j["system"]["category"]["value"] == "ritual":
      j["system"]["ritual"] = {"primary": {"check": ""}}
  if j["system"]["category"]["value"] == "focus" and\
      "focus" not in j["system"]["traits"]["value"]:
      j["system"]["traits"]["value"].append("focus")

  if re.match("sustained", j["system"]["duration"]["value"]):
      j["system"]["duration"]["sustained"] = True
  if j["system"]["duration"]["value"] == "sustained":
      j["system"]["duration"]["value"] = ""

  if j["system"].get("save"):
      v = j["system"]["save"]["value"]
      if j["system"]["save"]["basic"] == "basic":
          j["system"]["defense"] = {"save": {"statistic": v, "basic": True}}
      else:
          j["system"]["defense"] = {"save": {"statistic": v}}

  j["system"]["traits"]["traditions"] = j["system"]["traditions"]["value"]

  #print(json.dumps(j, indent=2))
  ldb.delete(key)
  ldb.put(key, json.dumps(j).encode())
ldb.close()

# 特技をコンバートする
# 旧DBを新PGで使用するため、旧→新にデータコンバートする。
ldb = plyvel.DB(pathLegacy+"feats-legacy", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  if j["system"]["traits"].get("value"):
      for v in j["system"]["traits"]["value"]:
          if v == "half-elf":
              j["system"]["traits"]["value"].append("aiuvarin")
          if v == "half-orc":
              j["system"]["traits"]["value"].append("dromaar") 
          if v == "aasimar" or v == "tiefling":
              j["system"]["traits"]["value"].append("nephilim")

  #print(json.dumps(j, indent=2))
  ldb.delete(key)
  ldb.put(key, json.dumps(j).encode())
ldb.close()

# legacyコンテンツをsystems/pf2e/packsに上書き
targets = {
  "actions": "actions-legacy",
  "ancestries": "ancestries-legacy",
  "ancestryfeatures": "ancestry-features-legacy",
  "backgrounds": "backgrounds-legacy",
  "classfeatures": "class-features-legacy",
  "classes": "classes-legacy",
  #"equipment-effects": "equipment-effects-legacy",
  #"equipment": "equipment-legacy", # 装備品はCompendium Browserでうまく表示されないため省略
  "feat-effects": "feat-effects-legacy",
  "feats": "feats-legacy",
  "heritages": "heritages-legacy",
  "spell-effects": "spell-effects-legacy",
  "spells": "spells-legacy",
  "other-effects": "other-effects-legacy",
}

for key in targets:
    shutil.rmtree(pathRemaster + key)
    shutil.copytree(pathLegacy + targets[key], pathRemaster + key)


# セーヴ有無を呪文説明文に表示
save_umu = '''
{{#if (eq spell.system.defense.save.statistic "reflex")}}
{{#if spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.Item.Spell.Defense.BasicSave"}} {{localize "PF2E.SavesReflex"}}</p>
{{/if}}
{{#unless spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.SavesReflex"}}</p>
{{/unless}}
{{/if}}
{{#if (eq spell.system.defense.save.statistic "will")}}
{{#if spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.Item.Spell.Defense.BasicSave"}} {{localize "PF2E.SavesWill"}}</p>
{{/if}}
{{#unless spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.SavesWill"}}</p>
{{/unless}}
{{/if}}
{{#if (eq spell.system.defense.save.statistic "fortitude")}}
{{#if spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.Item.Spell.Defense.BasicSave"}} {{localize "PF2E.SavesFortitude"}}</p>
{{/if}}
{{#unless spell.system.defense.save.basic}}
<p><strong>{{localize "PF2E.SavesHeader"}} </strong>
{{localize "PF2E.SavesFortitude"}}</p>
{{/unless}}
{{/if}}
'''

spell_desc_path = path + "templates/items/partials/spell-description-prepend.hbs"
if not os.path.isfile(spell_desc_path + ".bk"):
    shutil.copy2(spell_desc_path, spell_desc_path + ".bk")
    with open(spell_desc_path, mode="a") as f:
        print(save_umu, file=f)


character_tabs_path = path + "templates/actors/character/tabs/character.hbs"
if not os.path.isfile(character_tabs_path + ".bk"):
    shutil.copy2(character_tabs_path, character_tabs_path + ".bk")
    rep = ""
    with open(character_tabs_path, 'r') as f:
        r = f.read()
        rep = r.replace('pf2e.deities', 'z_pf2eja.fr-deities')
    with open(character_tabs_path, 'w') as f:
        print(rep, file=f)
