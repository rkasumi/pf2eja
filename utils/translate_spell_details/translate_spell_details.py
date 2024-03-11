import json
import plyvel
import shutil
import re
import os
from pprint import pprint
pathLegacy = "/home/yaginumad/userdata_pf/Data/modules/pf2e-legacy-content/packs/"

json_c = None
with open("../../compendium/pf2e.spells-srd.json", "r") as fh:
  json_c = json.load(fh)

duration_data = None
with open("./duration.json", "r") as fh:
  duration_data = json.load(fh)

range_data = None
with open("./range.json", "r") as fh:
  range_data = json.load(fh)

target_data = None
with open("./target.json", "r") as fh:
  target_data = json.load(fh)

time_data = None
with open("./time.json", "r") as fh:
  time_data = json.load(fh)

cost_data = None
with open("./cost.json", "r") as fh:
  cost_data = json.load(fh)

ritual_primary_data = None
with open("./ritual_primary.json", "r") as fh:
  ritual_primary_data = json.load(fh)

ritual_secondary_data = None
with open("./ritual_secondary.json", "r") as fh:
  ritual_secondary_data = json.load(fh)

ldb = plyvel.DB(pathLegacy+"spells-legacy", create_if_missing=False)
non_trans = {'duration': {}, 'range': {}, 'target': {}, 'time': {}, 'cost': {}, 'rp': {}, 'rs': {}}
for key, line in ldb:
  j = json.loads(line)
  if j['name'] in json_c['entries']:
    jpj = json_c['entries'][j['name']]
    # duration
    if j['system']['duration']['value'] != "": # 辞典に記載あり
      if j['system']['duration']['value'] in duration_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['duration'] = \
          duration_data[j['system']['duration']['value']]
      else:
        non_trans['duration'][j['system']['duration']['value']] = jpj['name']
    # range
    if j['system']['range']['value'] != "": # 辞典に記載あり
      if j['system']['range']['value'] in range_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['range'] = \
          range_data[j['system']['range']['value']]
      else:
        non_trans['range'][j['system']['range']['value']] = jpj['name']
    # target
    if j['system']['target']['value'] != "": # 辞典に記載あり
      if j['system']['target']['value'] in target_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['target'] = \
          target_data[j['system']['target']['value']]
      else:
        non_trans['target'][j['system']['target']['value']] = jpj['name']
    # time
    if j['system']['time']['value'] != "": # 辞典に記載あり
      if j['system']['time']['value'] in time_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['time'] = \
          time_data[j['system']['time']['value']]
      else:
        non_trans['time'][j['system']['time']['value']] = jpj['name']
    # cost
    if j['system']['cost']['value'] != "": # 辞典に記載あり
      if j['system']['cost']['value'] in cost_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['cost'] = \
          cost_data[j['system']['cost']['value']]
      else:
        non_trans['cost'][j['system']['cost']['value']] = jpj['name']
    # ritual.primary.check
    if 'ritual' in j['system']: # 辞典に記載あり
      if j['system']['ritual']['primary']['check'] in ritual_primary_data: # 対訳表に記載あり
        json_c['entries'][j['name']]['ritual_primary'] = \
          ritual_primary_data[j['system']['ritual']['primary']['check']]
      else:
        non_trans['rp'][j['system']['ritual']['primary']['check']] = jpj['name']
    # ritual.secondary.checks
    if 'ritual' in j['system']: # 辞典に記載あり
      if j['system']['ritual']['secondary']['checks'] in ritual_secondary_data: # 対訳表あり
        json_c['entries'][j['name']]['ritual_secondary'] = \
          ritual_secondary_data[j['system']['ritual']['secondary']['checks']]
      else:
        non_trans['rs'][j['system']['ritual']['secondary']['checks']] = jpj['name']
ldb.close()

with open("./pf2e.spells-srd.json", 'w', encoding='utf-8') as fh:
  json.dump(json_c, fh, indent=2, ensure_ascii=False)

pprint(non_trans)

