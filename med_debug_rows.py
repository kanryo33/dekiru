# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF)
def has_jp(s):
    return any(is_jp_char(c) for c in s)

def row_cluster(tokens, gap=3.0):
    tokens.sort(key=lambda w: (w[1], w[0]))
    rows = []
    cur = None
    for w in tokens:
        x0, y0, x1, y1, txt = w
        if cur is None or y0 - cur[1] > gap:
            cur = [y0, y1, []]
            rows.append(cur)
        cur[1] = max(cur[1], y1)
        cur[2].append((x0, y0, txt))
    out = []
    for r in rows:
        r[2].sort(key=lambda t: (t[1], t[0]))
        out.append((r[0], r[1], r[2]))
    return out

doc = pymupdf.open(r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト\英語.pdf')
page = doc[3]
words = page.get_text('words', sort=True)
left = [w[:5] for w in words if 45 < w[0] < 300 and w[1] > 55]
jp = [w for w in left if w[2] < 150 and has_jp(w[4])]
rows = row_cluster(jp)
print('=== 第4页 左栏 日语行（按y）===')
for i, (ry0, ry1, rtoks) in enumerate(rows):
    txt = ''.join(t[2] for t in rtoks)
    print(f'[{i}] y={ry0:6.1f}-{ry1:6.1f} [{txt}]  (tokens={len(rtoks)})')
