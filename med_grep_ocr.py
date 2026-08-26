# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ocr = json.load(open('med_zh_ocr.json', encoding='utf-8'))
check = ['グルメ','ポイント','簡易','なぜか','名産','最大','中古','学園','早口','ほっぺた','いざ','機関','気楽','社会保障','よさ','日数','未婚','エッセイ','驚き','便利さ','過程','バイオマス','カカオ豆','概要','永久','可能性','プラスチック','向き合う','野生','ファンクラブ','思い通り','電源','地熱','バブル','数値','上り下り','国語']
for t in check:
    hits = []
    for page, entries in ocr.items():
        for e in entries:
            for col in ['jp', 'zh']:
                v = e.get(col) or ''
                if t in v:
                    hits.append((page, col, v[:40]))
    print('==', t, '==', len(hits))
    for h in hits[:8]:
        print('   ', h)
