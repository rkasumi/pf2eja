import json
import plyvel
pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"

out = {}
ldb = plyvel.DB(pathLegacy+"feats-legacy", create_if_missing=False)
for key, line in ldb:
  j = json.loads(line)
  out[j['name']] = j
ldb.close()
print(json.dumps(out, indent=2))
