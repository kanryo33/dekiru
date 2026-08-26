# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
en = json.load(open('med_words_en.json', encoding='utf-8'))
bad = []
for k in sorted(en, key=int):
    for (kanji, kana, etxt) in en[k]:
        # 未闭合括号
        if kanji.count('（') != kanji.count('）') or kanji.count('(') != kanji.count(')'):
            bad.append((k, kanji))
        # 方括号
        elif '[' in kanji or ']' in kanji:
            bad.append((k, kanji))
print('格式问题词条:', len(bad))
for b in bad[:60]:
    print(' 课%s %s' % b)
