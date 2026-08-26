# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def norm_en(s):
    s = s.lower()
    s = re.sub(r'[^a-z\s]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

en = json.load(open('med_words_en.json', encoding='utf-8'))
zh_ocr = json.load(open('med_zh_ocr.json', encoding='utf-8'))

# 收集所有中文行 (en_norm, zh)
zh_rows = []
for page, entries in zh_ocr.items():
    for e in entries:
        if e['en'] and e['zh']:
            zh_rows.append((e['en'], e['zh'], page, e['side'], e['y']))

# 匹配：精确 norm_en 相等
matched = 0
unmatched = []
for k in sorted(en, key=int):
    for (kanji, kana, etxt) in en[k]:
        en_norm = norm_en(etxt)
        if not en_norm:
            unmatched.append((k, kanji, etxt, None))
            continue
        hits = [(z, p, s, y) for (e, z, p, s, y) in zh_rows if e == en_norm]
        if hits:
            matched += 1
        else:
            unmatched.append((k, kanji, etxt, None))

print(f'精确匹配: {matched} / {matched+len(unmatched)}')
print(f'未匹配: {len(unmatched)}')
for u in unmatched[:60]:
    print(f'  L{u[0]} {u[1]} | {u[2][:60]}')
