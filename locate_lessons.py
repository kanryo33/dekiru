# -*- coding: utf-8 -*-
# 定位三语行文本中每课的"ことば"起始行
import re

for name in ['英語', '中国語', 'ネパール語']:
    path = r'D:\できる日本語 单词卡\{}_lines.txt'.format(name)
    lines = open(path, encoding='utf-8').read().split('\n')
    print('=====', name, '=====')
    for i, ln in enumerate(lines):
        s = ln.replace(' ', '')
        if re.search(r'第\s*[0-9０-９一二三四五六七八九十]+\s*課', s) or re.search(r'^\s*[0-9]+\s*[私趣2-9]', s) is None and '[ことば]' in s:
            pass
        if 'ことば' in s or re.search(r'第\s*[0-9０-９一二三四五六七八九十]+\s*課', s):
            print(i+1, ':', ln[:50])
    print()
