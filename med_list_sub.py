# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
rows = json.load(open('med_trilingual.json', encoding='utf-8'))
print('=== sub 匹配全部（需核查） ===')
for r in rows:
    if r['src'] == 'sub':
        print('课%d %s | EN:%s | CN:%s' % (r['lesson'], r['kanji'], r['en'][:50], r['cn']))
