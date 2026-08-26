# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))
for k in sorted(en, key=int):
    e = [x[0] for x in en[k]]
    n = [x[0] for x in ne[k]]
    if e == n:
        print(f'第{k}课: {len(e)}词 一致')
    else:
        print(f'第{k}课: EN={len(e)} NE={len(n)} 不一致')
        # 找差异
        se, sn = set(e), set(n)
        only_en = [x for x in e if x not in sn]
        only_ne = [x for x in n if x not in se]
        print(f'   仅EN: {only_en[:8]}')
        print(f'   仅NE: {only_ne[:8]}')
