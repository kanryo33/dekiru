# -*- coding: utf-8 -*-
import pymupdf, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def segment(tokens):
    """按 x 间隙把同一行 token 分成段，返回 [(seg_text, x0)]"""
    if not tokens: return []
    tokens = sorted(tokens)
    segs = []
    cur = [tokens[0]]
    cur_x0 = tokens[0][0]
    for i in range(1, len(tokens)):
        if tokens[i][0] - tokens[i-1][1] > 25:  # 间隙阈值
            segs.append((cur, cur_x0))
            cur = [tokens[i]]
            cur_x0 = tokens[i][0]
        else:
            cur.append(tokens[i])
    segs.append((cur, cur_x0))
    return [( ' '.join(t[2] for t in toklist), x0) for toklist, x0 in segs]

for name, out in [('英語', 'ch2_英語_lines.txt'), ('中国語', 'ch2_中国語_lines.txt'), ('ネパール語', 'ch2_ネパール語_lines.txt')]:
    path = r'E:\教科書\できる日本語＆漢字たまご\初中級\語彙リスト\{}.pdf'.format(name)
    lines = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, start=1):
            words = page.get_text('words', sort=True)
            rows = {}
            for w in words:
                x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
                key = round(y0 / 3.0)
                rows.setdefault(key, []).append((x0, x1, txt))
            for key in sorted(rows):
                # 左栏段与右栏段（x<300 左, >=300 右）
                left_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 < 300]
                right_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 >= 300]
                for seg, x0 in segment(left_toks):
                    lines.append('L| ' + seg)
                for seg, x0 in segment(right_toks):
                    lines.append('R| ' + seg)
            lines.append('==== PAGE {} ===='.format(pno))
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(name, 'lines =', len(lines))
