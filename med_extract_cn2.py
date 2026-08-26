# -*- coding: utf-8 -*-
"""按坐标从中文PDF精确提取 (英文->中文) 官方映射"""
import pymupdf, json, sys, io, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
doc = pymupdf.open(r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト\中国語.pdf')

def classify(s):
    has_lat = bool(re.search(r'[A-Za-z]', s))
    has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3001\u3002\uff08\uff09\u2014\u30fb\uff1a\uff1b\u201c\u201d]', s))
    if has_lat and not has_cjk:
        return 'en'
    if has_cjk and not has_lat:
        return 'cn'
    return 'other'

all_pairs = []  # (page, en, cn)
for pno in range(len(doc)):
    d = doc[pno].get_text('dict')
    lines = []  # (y, x, kind, text)
    for b in d['blocks']:
        if 'lines' not in b:
            continue
        for ln in b['lines']:
            txt = ''.join(s['text'] for s in ln['spans']).strip()
            if not txt:
                continue
            x0, y0 = ln['bbox'][0], ln['bbox'][1]
            kind = classify(txt)
            if kind in ('en', 'cn'):
                lines.append((y0, x0, kind, txt))
    lines.sort(key=lambda t: (round(t[0]), t[1]))
    # 左右栏当前词条
    cur = {'L': None, 'R': None}
    page_pairs = []
    def settle(col):
        c = cur[col]
        if c and c['en'] and c['cn']:
            page_pairs.append((c['en'], c['cn']))
    for y, x, kind, txt in lines:
        col = 'L' if x < 300 else 'R'
        if kind == 'en':
            if cur[col] is not None and cur[col]['cn'] is None and cur[col]['en']:
                # 英文跨行续接
                cur[col]['en'] += ' ' + txt
            else:
                # 新词条：先结算旧的
                settle(col)
                cur[col] = {'en': txt, 'cn': None}
        elif kind == 'cn':
            if cur[col] is not None and cur[col]['cn'] is None and cur[col]['en']:
                cur[col]['cn'] = txt
            elif cur[col] is not None and cur[col]['cn']:
                cur[col]['cn'] += txt
            else:
                # 中文先于英文出现
                settle(col)
                cur[col] = {'en': '', 'cn': txt}
    settle('L')
    settle('R')
    for e, c in page_pairs:
        all_pairs.append((pno + 1, e, c))
    print('页%d: %d对' % (pno + 1, len(page_pairs)))

json.dump(all_pairs, open('med_zh_en_cn_map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('总对:', len(all_pairs))
