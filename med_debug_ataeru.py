# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF)
def is_kana_char(ch):
    o = ord(ch)
    return 0x3040 <= o <= 0x30FF
def has_jp(s):
    return any(is_jp_char(c) for c in s)
def has_kanji(s):
    return any(0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF for c in s)
def is_pure_kana(s):
    s2 = s.replace(' ', '').replace('　','')
    if not s2: return False
    return all(is_kana_char(c) or c in 'ー・、。()（）' for c in s2)

def row_cluster(tokens, gap=2.0):
    tokens.sort(key=lambda w: (w[1], w[0]))
    rows = []
    cur = None
    for w in tokens:
        x0, y0, x1, y1, txt = w
        if cur is None or y0 - cur[0] > gap:
            cur = [y0, y1, []]
            rows.append(cur)
        cur[1] = max(cur[1], y1)
        cur[2].append((x0, y0, txt))
    out = []
    for r in rows:
        r[2].sort(key=lambda t: t[0])
        out.append((r[0], r[1], r[2]))
    return out

doc = pymupdf.open(r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト\英語.pdf')
page = doc[3]
words = page.get_text('words', sort=True)
toks = [w[:5] for w in words if 300 <= w[0] < 595 and w[1] > 55]
jp = [w for w in toks if w[2] < 410 and has_jp(w[4])]
rows = row_cluster(jp)
for i, (ry0, ry1, rtoks) in enumerate(rows):
    txt = ''.join(t[2] for t in rtoks)
    if '与' in txt or 'える' in txt and ry0 > 500:
        print(f'[{i}] y={ry0:6.1f} [{txt}]')
        for t in rtoks:
            print(f'    x0={t[0]:6.1f} y0={t[1]:6.1f} [{t[2]}]')
