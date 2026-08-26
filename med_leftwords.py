# -*- coding: utf-8 -*-
import pymupdf, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
path = os.path.join(base, '英語.pdf')
with pymupdf.open(path) as doc:
    page = doc[3]  # 第4页
    words = page.get_text('words', sort=True)
    # 左栏 x<300, 按 y 精确排序
    left = sorted([w for w in words if w[0] < 300], key=lambda w: (round(w[1],1), w[0]))
    print('=== 第4页 左栏 words 按 y 排序 ===')
    for w in left:
        print(f'y={w[1]:7.1f} x={w[0]:6.1f} {w[4]}')
