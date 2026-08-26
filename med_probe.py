# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
for name in ['英語', '中国語', 'ネパール語']:
    path = os.path.join(base, name + '.pdf')
    with pymupdf.open(path) as doc:
        print(f'=== {name}.pdf ({doc.page_count}p) ===')
        # 探测若干页的布局
        for pi in [3, 4, 5, 10, 20, 40]:
            if pi >= doc.page_count: continue
            page = doc[pi]
            words = page.get_text('words', sort=True)
            xs = [w[0] for w in words]
            x1s = [w[2] for w in words]
            if not words:
                print(f'  第{pi+1}页: 无words')
                continue
            wmax = max(x1s)
            print(f'  第{pi+1}页: {len(words)} words, 页宽={page.rect.width:.0f}, word x0范围=[{min(xs):.0f},{max(xs):.0f}], x1max={wmax:.0f}')
            # 检测是否双栏：x0 直方图粗探
            left = sum(1 for w in words if w[0] < page.rect.width/2)
            right = sum(1 for w in words if w[0] >= page.rect.width/2)
            print(f'    左半words={left}, 右半words={right}')
            # 抽样文本
            txt = ' '.join(w[4] for w in words[:12])
            print(f'    样本: {txt[:120]}')
