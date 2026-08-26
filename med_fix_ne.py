# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
rows = json.load(open('med_trilingual.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))

def norm(s):
    if not s: return ''
    s = s.replace(' ', '').replace('\u3000', '').replace('〜', '～')
    for a, b in zip('０１２３４５６７８９', '0123456789'):
        s = s.replace(a, b)
    return s
def strip_bracket(s):
    return re.sub(r'[（(].*?[）)]', '', s)
def main_part(s):
    return re.split(r'[（(]', s)[0].strip()

# 构建 NE 索引（含 kana、去括号、main、去-）
ne_bykey = {}
ne_full = []
for k, items in ne.items():
    for (kanji, kana, netxt) in items:
        ne_full.append((kanji, kana, netxt))
        keys = {norm(kanji), norm(kana), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-','')), norm(kana.replace('-',''))}
        for kk in keys:
            if kk:
                ne_bykey.setdefault(kk, netxt)

def find_ne(kanji, kana):
    for key in [norm(kanji), norm(kana), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-',''))]:
        if key and key in ne_bykey:
            return ne_bykey[key]
    # sub 前缀
    c3 = norm(main_part(kanji))
    if c3 and len(c3) >= 2:
        for kan, kan2, ne_txt in ne_full:
            zmp = norm(main_part(kan))
            if zmp and len(zmp) >= 2 and (zmp.startswith(c3) or c3.startswith(zmp)) and abs(len(zmp)-len(c3)) <= 3:
                return ne_txt
    return ''

miss = []
for r in rows:
    r['ne'] = find_ne(r['kanji'], r['kana'])
    if not r['ne'].strip():
        miss.append((r['lesson'], r['kanji'], r['en'][:35]))
print('改进后尼语缺失:', len(miss))
for m in miss:
    print(' 课%d %s | EN:%s' % m)
json.dump(rows, open('med_trilingual.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
