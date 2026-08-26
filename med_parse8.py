# -*- coding: utf-8 -*-
import pymupdf, sys, io, os, re
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

def parse_page(page, side, pno):
    words = page.get_text('words', sort=True)
    if side == 'L':
        toks = [w for w in words if 45 < w[0] < 300 and w[1] > 55]
        jp_xmax = 150
    else:
        toks = [w for w in words if 300 <= w[0] < 595 and w[1] > 55]
        jp_xmax = 410
    jp_toks = [w[:5] for w in toks if w[0] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    rows = row_cluster(jp_toks)
    # 构建词条行：汉字行/片假名词条行；遇未闭合"（"吸收后续行直到闭合
    entry_rows = []  # (row_idx, y0, kanji)
    i = 0
    n = len(rows)
    while i < n:
        ry0, ry1, rtoks = rows[i]
        txt = ''.join(t[2] for t in rtoks)
        if is_pure_kana(txt):
            i += 1
            continue
        if not (has_kanji(txt) or (txt and any(0x30A0 <= ord(c) <= 0x30FF for c in txt))):
            i += 1
            continue
        # 括号闭合吸收：只吸收以"）"结尾的后续行（跨行括号闭合行）
        cur_txt = txt
        while cur_txt.count('（') > cur_txt.count('）') and i + 1 < n:
            nxt = rows[i+1]
            nxt_txt = ''.join(t[2] for t in nxt[2])
            if nxt[0] - ry0 > 25:
                break
            if not nxt_txt.rstrip().endswith('）'):
                break
            cur_txt += nxt_txt
            i += 1
        entry_rows.append((i, ry0, cur_txt))
        i += 1
    entries = []
    for ei, (i, y0, kanji) in enumerate(entry_rows):
        if kanji in ('［ことば］', '［できること］'): continue
        if 'ことば' in kanji and '［' in kanji: continue
        # 上方最近注音行
        kana = ''
        for j in range(i-1, -1, -1):
            rj0, rj1, rtoks = rows[j]
            if y0 - rj1 > 12: break
            t = ''.join(t[2] for t in rtoks)
            if is_pure_kana(t):
                kana = t; break
        # 翻译：y 在 [y0-10, y0+6] 的英文
        engs = [w for w in eng_toks if (y0-10) <= w[1] <= (y0+6)]
        engs.sort(key=lambda w: (w[1], w[0]))
        etxt = ' '.join(w[4] for w in engs)
        if not etxt:
            continue  # 栏目标题 / 页眉等无翻译内容
        entries.append((pno, y0, kanji, kana, etxt))
    return entries

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
with pymupdf.open(os.path.join(base, '英語.pdf')) as doc:
    kotoba, lessons = [], []
    for pno in range(len(doc)):
        page = doc[pno]
        for w in page.get_text('words', sort=True):
            if 'ことば' in w[4] and w[0] < 60:
                kotoba.append((pno, w[1])); break
        for w in page.get_text('words', sort=True):
            t = w[4].replace(' ', '')
            if re.fullmatch(r'[0-9０-９]+課', t) and w[1] < 80:
                lessons.append((pno, w[1], t)); break
    kotoba = kotoba[1:]
    ranges = []
    for i, (p, y) in enumerate(kotoba):
        nxt = None
        for (lp, ly, t) in lessons:
            if (lp > p) or (lp == p and ly > y):
                nxt = (lp, ly); break
        if nxt is None:
            nxt = (len(doc)-1, 9999)
        ranges.append(((p, y), nxt))
    for idx, ((p0, y0), (p1, y1)) in enumerate(ranges, 1):
        entries = []
        for pno in range(p0, p1+1):
            ymin = y0 if pno == p0 else 0
            ymax = y1 if pno == p1 else 9999
            for side in ['L', 'R']:
                for item in parse_page(doc[pno], side, pno):
                    pn, yy, kanji, kana, etxt = item
                    if ymin <= yy <= ymax:
                        entries.append(item)
        entries.sort(key=lambda t: (t[0], t[1]))
        print(f'== 第{idx}课 词条数={len(entries)} ==')
        for pno, yy, kanji, kana, etxt in entries:
            print(f'   p{pno+1} {kanji} ({kana}) <- {etxt[:55]}')
