# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def norm_en(s):
    s = s.lower()
    s = re.sub(r'[^a-z]', '', s)
    return s

en = json.load(open('med_words_en.json', encoding='utf-8'))
zh_ocr = json.load(open('med_zh_ocr.json', encoding='utf-8'))

# 收集所有中文行
zh_rows = []
for page, entries in zh_ocr.items():
    for e in entries:
        if e['en'] and e['zh']:
            zh_rows.append((norm_en(e['en']), e['zh'], page, e['side'], e['y'], e['en']))

def find_match(en_norm):
    # 精确
    exact = [z for (e, z, p, s, y, r) in zh_rows if e == en_norm]
    if exact:
        return exact[0], 'exact'
    # 子串（en_norm 含行 en，或行 en 含 en_norm），len>=6
    cands = []
    for (e, z, p, s, y, r) in zh_rows:
        if len(e) >= 6 and e in en_norm:
            cands.append((len(e), z))
        elif len(en_norm) >= 6 and en_norm in e:
            cands.append((len(en_norm), z))
    if cands:
        cands.sort(key=lambda t: -t[0])
        return cands[0][1], 'sub'
    return None, 'none'

matched = {'exact': 0, 'sub': 0}
unmatched = []
for k in sorted(en, key=int):
    for (kanji, kana, etxt) in en[k]:
        en_norm = norm_en(etxt)
        if not en_norm:
            unmatched.append((k, kanji, etxt, 'no-en'))
            continue
        z, how = find_match(en_norm)
        if z:
            matched[how] = matched.get(how, 0) + 1
        else:
            unmatched.append((k, kanji, etxt, 'none'))

print(f'匹配: exact={matched.get("exact",0)} sub={matched.get("sub",0)} 未匹配={len(unmatched)}')
print(f'总匹配率: {(matched.get("exact",0)+matched.get("sub",0))/2288*100:.1f}%')
for u in unmatched[:50]:
    print(f'  L{u[0]} {u[1]} | {u[2][:55]}')
