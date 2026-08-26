# -*- coding: utf-8 -*-
import pymupdf, os
base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
# 英语 PDF 第4、5页（第1课词汇区）
with pymupdf.open(os.path.join(base, '英語.pdf')) as doc:
    for pi in [3, 4]:
        page = doc[pi]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), alpha=False)
        pix.save(f'med_en_p{pi+1}.png')
        print(f'saved med_en_p{pi+1}.png', pix.width, pix.height)
