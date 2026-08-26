# -*- coding: utf-8 -*-
# 提取三个PDF的全部"词行"（日语词+翻译），用于人工整理缺失词翻译
import pymupdf

folder = r'D:\教科書\できる日本語＆漢字たまご\初級\語彙翻訳リスト'
for name in ['英語', '中国語', 'ネパール語']:
    doc = pymupdf.open(folder + '\\' + name + '.pdf')
    out = []
    for pno in range(doc.page_count):
        page = doc[pno]
        words = page.get_text('words', sort=False)
        left = [w for w in words if w[0] < 300]
        right = [w for w in words if w[0] >= 300]
        out.append('==== PAGE {} ===='.format(pno+1))
        for col_name, col in [('L', left), ('R', right)]:
            ws = sorted(col, key=lambda w: (round(w[1]), w[0]))
            cur, cury = [], None
            for w in ws:
                y = round(w[1])
                if cury is None or abs(y-cury) <= 3:
                    cur.append(w)
                    cury = y if cury is None else min(cury, y)
                else:
                    cur.sort(key=lambda z: z[0])
                    out.append('{} {}'.format(col_name, ' '.join(z[4] for z in cur)))
                    cur, cury = [w], y
            if cur:
                cur.sort(key=lambda z: z[0])
                out.append('{} {}'.format(col_name, ' '.join(z[4] for z in cur)))
    doc.close()
    with open(r'D:\できる日本語 单词卡\{}_lines.txt'.format(name), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(name, len(out))
