# -*- coding: utf-8 -*-
import pymupdf, sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF)

def has_jp(s):
    return any(is_jp_char(c) for c in s)

def is_pure_kana(s):
    s2 = s.replace(' ', '').replace('　','')
    if not s2: return False
    return all(0x3040 <= ord(c) <= 0x30FF or c in 'ー・、。' for c in s2)

def cluster(tokens, gap):
    tokens.sort(key=lambda w: (w[1], w[0]))
    clusters = []
    cur = None
    for w in tokens:
        x0, y0, x1, y1, txt = w
        if cur is None or y0 - cur[4] > gap:
            cur = [y0, y1, y1, [], y0]   # y0,y1,bottom,tokens,y0max
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

def parse_page(page, side):
    words = page.get_text('words', sort=True)
    if side == 'L':
        toks = [w for w in words if 45 < w[0] < 300 and w[1] > 55]
        jp_xmax = 150
    else:
        toks = [w for w in words if 300 <= w[0] < 595 and w[1] > 55]
        jp_xmax = 410
    jp_toks = [w[:5] for w in toks if w[2] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    jp_clusters = cluster(jp_toks, 8.0)
    entries = []
    for jy0, jy1, jtoks in jp_clusters:
        ys = sorted(set(round(t[1],1) for t in jtoks))
        kana, kanji = '', ''
        if len(ys) >= 2:
            yk = ys[0]
            upper = ''.join(t[2] for t in jtoks if abs(t[1]-yk) < 2.0)
            lower = ''.join(t[2] for t in jtoks if abs(t[1]-ys[-1]) < 2.0)
            if is_pure_kana(upper):
                kana, kanji = upper, lower
            else:
                kanji = upper + lower
        else:
            kanji = ''.join(t[2] for t in jtoks)
        if not kanji: continue
        engs = [w for w in eng_toks if (jy0-10) <= w[1] <= (jy1+10)]
        engs.sort(key=lambda w: (w[1], w[0]))
        eng_txt = ' '.join(w[4] for w in engs)
        entries.append((kanji, kana, eng_txt))
    return entries

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
with pymupdf.open(os.path.join(base, '英語.pdf')) as doc:
    for side in ['L', 'R']:
        entries = parse_page(doc[3], side)
        print(f'===== {side}栏 第4页 词条数={len(entries)} =====')
        for kanji, kana, eng in entries:
            print(f'  [{kanji}] ({kana})  <-  {eng[:70]}')
