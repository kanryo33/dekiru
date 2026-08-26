# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def segment(tokens, gap=25):
    if not tokens: return []
    tokens = sorted(tokens)
    segs = []
    cur = [tokens[0]]
    cur_x0 = tokens[0][0]
    for i in range(1, len(tokens)):
        if tokens[i][0] - tokens[i-1][1] > gap:
            segs.append((cur, cur_x0))
            cur = [tokens[i]]
            cur_x0 = tokens[i][0]
        else:
            cur.append(tokens[i])
    segs.append((cur, cur_x0))
    return [(' '.join(t[2] for t in toklist), x0) for toklist, x0 in segs]

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
path = os.path.join(base, '英語.pdf')
L, R = [], []
with pymupdf.open(path) as doc:
    for pno, page in enumerate(doc, start=1):
        words = page.get_text('words', sort=True)
        rows = {}
        for w in words:
            x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
            key = round(y0 / 3.0)
            rows.setdefault(key, []).append((x0, x1, txt))
        for key in sorted(rows):
            left_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 < 300]
            right_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 >= 300]
            for seg, x0 in segment(left_toks):
                L.append((pno, seg))
            for seg, x0 in segment(right_toks):
                R.append((pno, seg))

print('左栏前 100 行:')
for i, (pno, seg) in enumerate(L[:100], 1):
    print(f'{i:3d} p{pno}: {seg}')
