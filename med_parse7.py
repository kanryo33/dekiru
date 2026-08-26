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

def parse_page(page, side, pno):
    words = page.get_text('words', sort=True)
    if side == 'L':
        toks = [w for w in words if 45 < w[0] < 300 and w[1] > 55]
        jp_xmax = 150
    else:
        toks = [w for w in words if 300 <= w[0] < 595 and w[1] > 55]
        jp_xmax = 410
    jp_toks = [w[:5] for w in toks if w[2] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    # 翻译块（gap=14）
    eng_toks.sort(key=lambda w: (w[1], w[0]))
    eblocks = []
    cur = None
    for w in eng_toks:
        if cur is None or w[1] - cur[1] > 14:
            cur = [w[1], w[1], []]
            eblocks.append(cur)
        cur[1] = max(cur[1], w[1])
        cur[2].append(w)
    # 日语行
    rows = row_cluster(jp_toks)
    # 翻译块配对：找与每个翻译块中心最近的日语行群
    entries = []
    used_rows = set()
    for (ey0, ey1, etoks) in eblocks:
        ec = (ey0 + ey1) / 2
        # 收集 y 距翻译块中心 ±20 的日语行
        cand = []
        for ri, (ry0, ry1, rtoks) in enumerate(rows):
            if ri in used_rows: continue
            rc = (ry0 + ry1) / 2
            if abs(rc - ec) <= 20:
                cand.append((ri, rc, ry0, ry1, rtoks))
        if not cand: continue
        cand.sort(key=lambda c: abs(c[1]-ec))
        # 取最近的 1-2 行（注音+汉字）
        ri, rc, ry0, ry1, rtoks = cand[0]
        # 该行是注音还是汉字？
        txt0 = ''.join(t[2] for t in rtoks)
        used_rows.add(ri)
        kana, kanji = '', ''
        if is_pure_kana(txt0):
            kana = txt0
            # 找下一行（汉字）
            nxt = None
            for ri2, (ry0b, ry1b, rtoks2) in enumerate(rows):
                if ri2 in used_rows or ri2 == ri: continue
                if ry0b > ry0 and ry0b - ry1 < 30:
                    nxt = (ri2, ''.join(t[2] for t in rtoks2), ry0b)
                    break
            if nxt and has_kanji(nxt[1]):
                kanji = nxt[1]
                used_rows.add(nxt[0])
            else:
                kanji = txt0
        else:
            kanji = txt0
        if not kanji: continue
        if kanji in ('［ことば］', '［できること］'): continue
        if 'ことば' in kanji and '［' in kanji: continue
        etxt = ' '.join(t[4] for t in sorted(etoks, key=lambda w: (w[1], w[0])))
        entries.append((pno, ec, kanji, kana, etxt))
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
                    # parse_page 返回整页，这里需要按 ymin/ymax 过滤
                    pn, ec, kanji, kana, etxt = item
                    if ymin <= ec <= ymax:
                        entries.append(item)
        entries.sort(key=lambda t: (t[0], t[1]))
        print(f'== 第{idx}课 词条数={len(entries)} ==')
        for pno, yy, kanji, kana, etxt in entries:
            print(f'   p{pno+1} {kanji} ({kana}) <- {etxt[:55]}')
