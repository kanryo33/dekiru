# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
zh = json.load(open('med_zh_read.json', encoding='utf-8'))
check = ['実際','グルメ','簡易','なぜか','名産','最大','特産','中古','学園','早口','わくわく','はらはら','しょんぼり','ほっぺた','いざ','機関','気楽','社会保障','目覚める','ポイント','うっかり','印象的','熱気','どきどき','もの','向き合う','プラスチック','感じ','永久','便利さ','日数','概要','よさ','育休','言葉','線','育児']
for t in check:
    hits = []
    for page, entries in zh.items():
        for (jp, cn) in entries:
            if t in jp:
                hits.append((page, jp, cn))
    print('==', t, '==')
    for h in hits[:6]:
        print('   ', h)
