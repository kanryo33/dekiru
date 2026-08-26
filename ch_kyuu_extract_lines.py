# -*- coding: utf-8 -*-
import pymupdf, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for name, out in [('英語', 'chuukyuu_英語_lines.txt'), ('中国語', 'chuukyuu_中国語_lines.txt'), ('ネパール語', 'chuukyuu_ネパール語_lines.txt')]:
    path = r'E:\教科書\できる日本語＆漢字たまご\初中級\語彙リスト\{}.pdf'.format(name)
    lines = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, start=1):
            words = page.get_text('words', sort=True)
            # 按 y 坐标分组（容差 3），再按 x 排序；x<300 为左栏，>=300 为右栏
            rows = {}
            for w in words:
                x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
                key = round(y0 / 3.0)
                rows.setdefault(key, []).append((x0, txt))
            for key in sorted(rows):
                left = [t for x, t in sorted(rows[key]) if x < 300]
                right = [t for x, t in sorted(rows[key]) if x >= 300]
                def col_text(col):
                    # 合并时在相邻文本间加空格（同一行的不同词）
                    return ' '.join(col) if col else ''
                lt = col_text(left)
                rt = col_text(right)
                line = ''
                if lt and rt:
                    line = 'L ' + lt + ' | R ' + rt
                elif lt:
                    line = 'L ' + lt
                elif rt:
                    line = 'R ' + rt
                if line:
                    lines.append(line)
            lines.append('==== PAGE {} ===='.format(pno))
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(name, 'lines =', len(lines))
