# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'chuukyuu_words.py'
lines = open(path, encoding='utf-8').read().split('\n')

# (kanji 精确匹配, 新 ne)
fixes = [
    ('"kanji":"イメージ・する"', 'कल्पना गर्नु'),
    ('"kanji":"もう～（例：もう一杯）"', 'अर्को ～ (जस्तै: अर्को एक कप)'),
    ('"kanji":"おばさん"', 'काकी'),
    ('"kanji":"水道"', 'पानीको धारा'),
    ('"kanji":"大きさ"', 'आकार'),
    ('"kanji":"ハート"', 'मुटुको आकार'),
    ('"kanji":"それに"', 'अनि त्यसका साथै'),
    ('"kanji":"ミステリー"', 'रहस्य / मिस्ट्री'),
    ('"kanji":"遠慮・する"', 'नम्रतापूर्वक अस्वीकार गर्नु'),
    ('"kanji":"シール"', 'स्टिकर'),
    ('"kanji":"ツイン"', 'ट्विन'),
    ('"kanji":"ポーチ"', 'पाउच / थैली'),
    ('"kanji":"元気"', 'सञ्चो'),
    ('"kanji":"さす"', 'छाता लगाउनु / उघार्नु'),
    ('"kanji":"気にする"', 'ध्यान गर्नु'),
    ('"kanji":"取り組む"', 'मिहिनेत गर्नु'),
]

changed = 0
out = []
for i, line in enumerate(lines, 1):
    newline = line
    for mark, new_ne in fixes:
        if mark in line:
            old_ne = re.search(r'"ne":"[^"]*"', line)
            old_val = old_ne.group(0) if old_ne else '(无)'
            newline = re.sub(r'"ne":"[^"]*"', '"ne":"' + new_ne + '"', line)
            print(f'L{i} 匹配 {mark}')
            print(f'    旧: {old_val}')
            print(f'    新: "ne":"{new_ne}"')
            changed += 1
            break
    out.append(newline)

print(f'\n共修改 {changed} 行')
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print('已写回 chuukyuu_words.py')
