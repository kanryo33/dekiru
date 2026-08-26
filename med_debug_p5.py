# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF)

def has_jp(s):
    return any(is_jp_char(c) for c in s)

def cluster(tokens, gap):
    tokens.sort(key=lambda w: (w[1], w[0]))
    clusters = []
    cur = None
    for w in tokens:
        x0, y0, x1, y1, txt = w
        if cur is None or y0 - cur[4] > gap:
            cur = [y0, y1, y1, [], y0]
            clusters.append(cur)
        cur[1] = max(cur[1], y1)
        cur[2] = max(cur[2], y1)
        cur[4] = max(cur[4], y0)
        cur[3].append((x0, y0, txt))
    out = []
    for c in clusters:
        c[3].sort(key=lambda t: (t[1], t[0]))
        out.append((c[0], c[1], c[3]))
    return out

doc = pymupdf.open(r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト\英語.pdf')
page = doc[4]  # p5
words = page.get_text('words', sort=True)
left = [w[:5] for w in words if 45 < w[0] < 300 and w[1] > 55]
jp_l = [w for w in left if w[2] < 150 and has_jp(w[4])]
eng_l = [w for w in left if w[0] >= 150]
jp_c = cluster(jp_l, 8.0)
eng_c = cluster(eng_l, 14.0)
print('=== p5 左栏 日语块 ===')
for i, (y0, y1, toks) in enumerate(jp_c):
    txt = ''.join(t[2] for t in sorted(toks, key=lambda t:(t[1],t[0])))
    print(f'  [{i}] y={y0:6.1f}-{y1:6.1f} {txt}')
print('=== p5 左栏 翻译块 ===')
for i, (y0, y1, toks) in enumerate(eng_c):
    tt = sorted(toks, key=lambda w:(w[1],w[0]))
    print(f'  [{i}] y={y0:6.1f}-{y1:6.1f} {" ".join(t[4] for t in tt)}')
