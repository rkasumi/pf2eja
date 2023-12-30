import json
import plyvel
import shutil
# 本PG実行後にfvtt再起動すること

pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"
pathRemaster = "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/"

# 呪文リストをコンバートする
#   旧： system.traditions.valueに体系(秘術、信仰、始原、伝承)が記録
#   新： syste.traits.traditionsに体系が記録
# 旧DBを新PGで使用するため、旧→新にデータコンバートする。
ldb = plyvel.DB(pathLegacy+"spells-legacy", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  j["system"]["traits"]["traditions"] = j["system"]["traditions"]["value"]
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
