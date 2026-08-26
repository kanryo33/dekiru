# -*- coding: utf-8 -*-
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
for name in ['英語', '中国語', 'ネパール語']:
    path = os.path.join(base, name + '.pdf')
    with pymupdf.open(path) as doc:
        print(f'=== {name}.pdf: {doc.page_count} 页 ===')
        # 提取前 3 页文本看结构
        for pi in range(min(3, doc.page_count)):
            page = doc[pi]
            text = page.get_text('text', sort=True)
            print(f'--- 第{pi+1}页 (len={len(text)}) ---')
            print(text[:1500])
            print('...')
