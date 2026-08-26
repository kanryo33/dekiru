# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
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

def cluster(tokens, gap=4.0):
    """按 y 聚类 tokens → [(y0, y1, [texts sorted by x])]"""
    if not tokens: return []
    tokens.sort(key=lambda w: (w[1], w[0]))
    clusters = []
    cur = None
    for w in tokens:
        x0, y0, x1, y1, txt = w
        if cur is None or y0 - cur[2] > gap:
            cur = [y0, y1, y1, []]
            clusters.append(cur)
        cur[1] = max(cur[1], y1)
        cur[2] = max(cur[2], y1)
        cur[3].append((x0, y0, txt))
    out = []
    for c in clusters:
        c[3].sort(key=lambda t: (t[1], t[0]))
        txt = ''.join(t[2] for t in c[3])
        out.append((c[0], c[1], txt))
    return out

def parse_page(page, side):
    words = page.get_text('words', sort=True)
    if side == 'L':
        toks = [w for w in words if w[0] < 300 and w[1] > 55]  # 跳过页眉
        jp_xmax = 150
    else:
        toks = [w for w in words if w[0] >= 300 and w[1] > 55]
        jp_xmax = 700
    jp_toks = [w[:5] for w in toks if w[0] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    # 过滤页码/页眉
    jp_toks = [w for w in jp_toks if not re_fullnum(w[4])]
    eng_toks = [w for w in eng_toks if not re_fullnum(w[4])]
    jp_clusters = cluster(jp_toks, 4.0)
    eng_clusters = cluster(eng_toks, 3.5)
    # 词条对齐：每个 eng 块对应一个词条，找下方最近 jp 块为汉字，上方最近 jp 块为注音
    entries = []
    used = set()
    for ey0, ey1, etxt in eng_clusters:
        # 汉字块：下方最近的 jp 块（y >= ey0, 差 < 8）
        kanji = None
        for i, (jy0, jy1, jtxt) in enumerate(jp_clusters):
            if i in used: continue
            if jy0 >= ey0 and jy0 - ey0 < 8:
                kanji = (i, jtxt)
                break
        # 注音块：上方最近的 jp 块（y < ey0, 差 < 8, 纯假名）
        kana = ''
        for jy0, jy1, jtxt in jp_clusters:
            if jy0 < ey0 and ey0 - jy0 < 8 and is_pure_kana(jtxt):
                kana = jtxt.replace(' ', '')
                break
        if kanji:
            used.add(kanji[0])
            entries.append((kanji[1], kana, etxt))
        else:
            entries.append(('', kana, etxt))
    return entries

def re_fullnum(s):
    return s.strip().isdigit()

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
with pymupdf.open(os.path.join(base, '英語.pdf')) as doc:
    for side in ['L', 'R']:
        entries = parse_page(doc[3], side)
        print(f'===== {side}栏 第4页 词条数={len(entries)} =====')
        for kanji, kana, eng in entries:
            print(f'  [{kanji}] ({kana})  <-  {eng[:60]}')
