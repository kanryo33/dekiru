# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
rows = json.load(open('med_trilingual.json', encoding='utf-8'))
nene = [r for r in rows if not r['ne'].strip()]
print('尼语缺失:', len(nene))
for r in nene:
    print('课%d %s | EN:%s | CN:%s' % (r['lesson'], r['kanji'], r['en'][:40], r['cn'][:30]))
