import json
import plyvel
import shutil
import re
import os
# 本PG実行後にfvtt再起動すること
path = "/home/yaginumad/userdata_pf/Data/systems/pf2e/"
pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"
pathRemaster = "/home/yaginumad/userdata_pf/Data/systems/pf2e/packs/"

ldb = plyvel.DB(pathLegacy+"class-features-legacy", create_if_missing=False)
#ldb = plyvel.DB(pathRemaster+"equipment", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)

  print(json.dumps(j, indent=2))
ldb.close()
