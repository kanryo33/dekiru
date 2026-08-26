# -*- coding: utf-8 -*-
import pymupdf, sys, io, os, re, json
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

def match_translation_block(eng_toks, jp_blocks):
    """以翻译块为锚点配对日语词块。返回 {jp_block_index: eng_text}"""
    if not eng_toks or not jp_blocks: return {}
    # 翻译 token 聚类成块（gap=14：跨行13合并，词条间距17+分开）
    eng_toks.sort(key=lambda w: (w[1], w[0]))
    blocks = []
    cur = None
    for w in eng_toks:
        if cur is None or w[1] - cur[1] > 14:
            cur = [w[1], w[1], []]
            blocks.append(cur)
        cur[1] = max(cur[1], w[1])
        cur[2].append(w)
    result = {}
    used_blocks = set()
    # 对每个日语块，找最近且未被占用的翻译块
    for bi, (bj0, bj1, btoks) in enumerate(jp_blocks):
        best = None
        for ti, (ty0, ty1, ttoks) in enumerate(blocks):
            if ti in used_blocks: continue
            # 块中心距离
            center_b = (bj0 + bj1) / 2
            center_t = (ty0 + ty1) / 2
            d = abs(center_b - center_t)
            if best is None or d < best[1]:
                best = (ti, d)
        if best:
            ti, d = best
            if d <= 15:
                used_blocks.add(ti)
                ttoks_sorted = sorted(blocks[ti][2], key=lambda w: (w[1], w[0]))
                result[bi] = ' '.join(w[4] for w in ttoks_sorted)
    return result

def parse_region(page, side, y_min, y_max, pno):
    words = page.get_text('words', sort=True)
    if side == 'L':
        toks = [w for w in words if 45 < w[0] < 300 and y_min <= w[1] <= y_max]
        jp_xmax = 150
    else:
        toks = [w for w in words if 300 <= w[0] < 595 and y_min <= w[1] <= y_max]
        jp_xmax = 410
    jp_toks = [w[:5] for w in toks if w[2] < jp_xmax and has_jp(w[4])]
    eng_toks = [w[:5] for w in toks if w[0] >= jp_xmax]
    eng_toks.sort(key=lambda w: (w[1], w[0]))
    jp_clusters = cluster(jp_toks, 8.0)
    entries = []
    for bi, (jy0, jy1, jtoks) in enumerate(jp_clusters):
        ys = sorted(set(round(t[1],1) for t in jtoks))
        kana, kanji = '', ''
        if len(ys) >= 2:
            yk = ys[0]
            upper_toks = sorted([t for t in jtoks if abs(t[1]-yk) < 2.0], key=lambda t: t[0])
            lower_toks = sorted([t for t in jtoks if abs(t[1]-ys[-1]) < 2.0], key=lambda t: t[0])
            upper = ''.join(t[2] for t in upper_toks)
            lower = ''.join(t[2] for t in lower_toks)
            if is_pure_kana(upper):
                kana, kanji = upper, lower
            else:
                kanji = upper + lower
        else:
            kanji = ''.join(t[2] for t in sorted(jtoks, key=lambda t: t[0]))
        if not kanji: continue
        if kanji in ('［ことば］', '［できること］'): continue
        entries.append((bi, pno, jy0, kanji, kana))
    # 用翻译块配对
    eng_map = match_translation_block(eng_toks, jp_clusters)
    out = []
    for bi, pno, jy0, kanji, kana in entries:
        eng_txt = eng_map.get(bi, '')
        if not eng_txt and not kana:
            continue
        out.append((pno, jy0, kanji, kana, eng_txt))
    return out

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
    all_lessons = {}
    for idx, ((p0, y0), (p1, y1)) in enumerate(ranges, 1):
        entries = []
        for pno in range(p0, p1+1):
            ymin = y0 if pno == p0 else 0
            ymax = y1 if pno == p1 else 9999
            for side in ['L', 'R']:
                entries.extend(parse_region(doc[pno], side, ymin, ymax, pno))
        entries.sort(key=lambda t: (t[0], t[1]))
        all_lessons[idx] = entries
        print(f'== 第{idx}课 词条数={len(entries)} ==')
        for pno, yy, kanji, kana, eng in entries:
            print(f'   p{pno+1} {kanji} ({kana}) <- {eng[:55]}')
