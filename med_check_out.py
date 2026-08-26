# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
rows = json.load(open('med_trilingual.json', encoding='utf-8'))
no_ne = [r for r in rows if not r['ne']]
print('无尼语:', len(no_ne))
for r in no_ne[:20]:
    print(' ', r['lesson'], r['kanji'], '|', r['en'])
print('=== 每课抽查（前2词条） ===')
cur = None
for r in rows:
    if r['lesson'] != cur:
        cur = r['lesson']
        for r2 in rows:
            if r2['lesson'] == cur and r2['no'] <= 2:
                print('课%d: %s | %s | CN:%s | NE:%s' % (cur, r2['kanji'], r2['en'][:30], r2['cn'][:20], r2['ne'][:20]))
