# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))

def align(en_list, ne_list):
    """两指针顺序对齐，返回 [(kanji, (en_kana,en_txt), (ne_txt or None), flag)]"""
    res = []
    i = j = 0
    while i < len(en_list):
        e = en_list[i]  # (kanji, kana, txt)
        if j < len(ne_list) and ne_list[j][0] == e[0]:
            res.append((e[0], (e[1], e[2]), ne_list[j][2], ''))
            i += 1; j += 1
        else:
            found = None
            for k in range(j, min(j + 6, len(ne_list))):
                if ne_list[k][0] == e[0]:
                    found = k; break
            if found is not None:
                for k in range(j, found):
                    res.append(('__EXTRA_NE__', (ne_list[k][1], ''), ne_list[k][2], 'EXTRA_NE'))
                res.append((e[0], (e[1], e[2]), ne_list[found][2], ''))
                i += 1; j = found + 1
            else:
                res.append((e[0], (e[1], e[2]), None, 'NO_NE'))
                i += 1
    while j < len(ne_list):
        res.append(('__EXTRA_NE__', (ne_list[j][1], ''), ne_list[j][2], 'EXTRA_NE'))
        j += 1
    return res

total_missing = 0
total_extra = 0
for k in sorted(en, key=int):
    e = en[k]
    n = ne.get(k, [])
    r = align(e, n)
    miss = sum(1 for x in r if x[3] == 'NO_NE')
    extra = sum(1 for x in r if x[3] == 'EXTRA_NE')
    total_missing += miss
    total_extra += extra
    print(f'第{k}课: {len(r)}条, NO_NE={miss}, EXTRA_NE={extra}')
    if miss or extra:
        for x in r:
            if x[3]:
                print(f'   [{x[3]}] {x[0]} <- {x[2][:30] if x[2] else ""}')
print(f'TOTAL 缺失={total_missing}, 多余NE={total_extra}')

# 保存对齐结果
out = {}
for k in sorted(en, key=int):
    r = align(en[k], ne.get(k, []))
    out[k] = [(kanji, en_kana, en_txt, ne_txt) for kanji, (en_kana, en_txt), ne_txt, flag in r]
json.dump(out, open('med_align_en_ne.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
