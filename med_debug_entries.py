# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF)
def has_jp(s):
    return any(is_jp_char(c) for c in s)
def is_kana_char(ch):
    o = ord(ch)
    return 0x3040 <= o <= 0x30FF
def is_pure_kana(s):
    s2 = s.replace(' ', '').replace('　','')
    if not s2: return False
    return all(is_kana_char(c) or c in 'ー・、。()（）' for c in s2)
def has_kanji(s):
    return any(0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF for c in s)

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
# p4 右栏 + p5 左栏 的 entry rows
for pno in [3, 4]:
    page = doc[pno]
    words = page.get_text('words', sort=True)
    if pno == 3:
        toks = [w[:5] for w in words if 300 <= w[0] < 595 and w[1] > 55]
        jp_xmax = 410
    else:
        toks = [w[:5] for w in words if 45 < w[0] < 300 and w[1] > 55]
        jp_xmax = 150
    jp = [w for w in toks if w[2] < jp_xmax and has_jp(w[4])]
    rows = row_cluster(jp)
    print(f'=== p{pno+1} 汉字行 ===')
    for i, (ry0, ry1, rtoks) in enumerate(rows):
        txt = ''.join(t[2] for t in rtoks)
        if is_pure_kana(txt): continue
        if has_kanji(txt) or (txt and any(0x30A0<=ord(c)<=0x30FF for c in txt)):
            print(f'  [{i}] y={ry0:6.1f} [{txt}]')
