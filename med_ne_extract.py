# -*- coding: utf-8 -*-
"""中级英语 PDF 全课词条解析 → med_words_ne.json"""
import pymupdf, sys, io, os, re, json
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
        toks = [w for w in words if 45 < w[0] < 300 and w[1] > 85]
        jp_xmax = 150
    else:
        toks = [w for w in words if 300 <= w[0] < 595 and w[1] > 85]
        jp_xmax = 410
    jp_toks = [w[:5] for w in toks if w[0] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    rows = row_cluster(jp_toks)
    entry_rows = []
    i = 0
    n = len(rows)
    while i < n:
        ry0, ry1, rtoks = rows[i]
        txt = ''.join(t[2] for t in rtoks)
        height = ry1 - ry0
        # 注音小字（高 < 9px）跳过
        if height < 9:
            i += 1
            continue
        if not has_jp(txt):
            i += 1
            continue
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
        if re.match(r'第\d+課', kanji.replace(' ', '')) or re.match(r'第[0-9０-９]+課', kanji):
            continue
        kana = ''
        for j in range(i-1, -1, -1):
            rj0, rj1, rtoks = rows[j]
            if y0 - rj1 > 12: break
            t = ''.join(t[2] for t in rtoks)
            if is_pure_kana(t) and (rj1 - rj0) < 9:
                kana = t; break
        engs = [w for w in eng_toks if (y0-10) <= w[1] <= (y0+6)]
        engs.sort(key=lambda w: (w[1], w[0]))
        etxt = ' '.join(w[4] for w in engs)
        if not etxt:
            continue
        entries.append((pno, y0, kanji, kana, etxt))
    return entries

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
with pymupdf.open(os.path.join(base, 'ネパール語.pdf')) as doc:
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
    kotoba = [k for k in kotoba if k[0] >= 3]
    ranges = []
    for i, (p, y) in enumerate(kotoba):
        nxt = None
        for (lp, ly, t) in lessons:
            if (lp > p) or (lp == p and ly > y):
                nxt = (lp, ly); break
        if nxt is None:
            nxt = (len(doc)-1, 9999)
        ranges.append(((p, y), nxt))
    all_lessons = {}
    for idx, ((p0, y0), (p1, y1)) in enumerate(ranges, 1):
        entries_L, entries_R = [], []
        for pno in range(p0, p1+1):
            ymin = y0 if pno == p0 else 0
            ymax = y1 if pno == p1 else 9999
            for item in parse_page(doc[pno], 'L', pno):
                pn, yy, kanji, kana, etxt = item
                if ymin <= yy <= ymax:
                    entries_L.append(item)
            for item in parse_page(doc[pno], 'R', pno):
                pn, yy, kanji, kana, etxt = item
                if ymin <= yy <= ymax:
                    entries_R.append(item)
        # 逐栏合并：先左栏（按页、y），再右栏（按页、y）
        entries_L.sort(key=lambda t: (t[0], t[1]))
        entries_R.sort(key=lambda t: (t[0], t[1]))
        all_lessons[idx] = [(kanji, kana, etxt) for pno, yy, kanji, kana, etxt in entries_L + entries_R]
    with open('med_words_ne.json', 'w', encoding='utf-8') as f:
        json.dump(all_lessons, f, ensure_ascii=False, indent=1)
    total = 0
    for k in sorted(all_lessons, key=int):
        n = len(all_lessons[k])
        total += n
        print(f'第{k}课: {n} 词条')
    print(f'TOTAL: {total}')
