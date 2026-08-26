# -*- coding: utf-8 -*-
"""中文列对齐：用英语翻译 + 日语词条 匹配英语PDF词表"""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def norm_en(s):
    return re.sub(r'[^a-z]', '', s.lower())

def jp_clean(s):
    # 提取中文/汉字部分（image-ocr jp列）
    return re.sub(r'[^一-龥ぁ-んァ-ヶ0-9～（）\-・]', '', s)

en = json.load(open('med_words_en.json', encoding='utf-8'))
zh_ocr = json.load(open('med_zh_ocr.json', encoding='utf-8'))

zh_rows = []
for page, entries in zh_ocr.items():
    for e in entries:
        if e['en'] and e['zh']:
            zh_rows.append({'en': norm_en(e['en']), 'zh': e['zh'], 'jp': jp_clean(e['jp']),
                            'page': page, 'y': e['y']})

# 词条列表（全册）
all_words = []
for k in sorted(en, key=int):
    for (kanji, kana, etxt) in en[k]:
        all_words.append({'lesson': k, 'kanji': kanji, 'kana': kana, 'en': etxt,
                          'en_norm': norm_en(etxt)})

# 逐词匹配
used = set()
for w in all_words:
    w['zh'] = None
    w['zh_src'] = None
    en_n = w['en_norm']
    if not en_n:
        continue
    # 1. en 精确
    cand = [i for i, r in enumerate(zh_rows) if r['en'] == en_n and i not in used]
    if cand:
        w['zh'] = zh_rows[cand[0]]['zh']; w['zh_src'] = 'en_exact'
        used.add(cand[0]); continue
    # 2. en 子串
    best = None
    for i, r in enumerate(zh_rows):
        if i in used: continue
        e = r['en']
        if len(e) >= 6 and e in en_n:
            if best is None or len(e) > len(zh_rows[best]['en']):
                best = i
    if best is not None:
        w['zh'] = zh_rows[best]['zh']; w['zh_src'] = 'en_sub'
        used.add(best); continue
    # 3. jp 词条匹配（去注音/括号）
    kanji_clean = jp_clean(w['kanji'].split('（')[0].split('(')[0])
    if len(kanji_clean) >= 2:
        cand = [i for i, r in enumerate(zh_rows) if i not in used and kanji_clean in r['jp']]
        if cand:
            w['zh'] = zh_rows[cand[0]]['zh']; w['zh_src'] = 'jp'
            used.add(cand[0]); continue

matched = sum(1 for w in all_words if w['zh'])
print(f'匹配: {matched}/{len(all_words)} ({matched/len(all_words)*100:.1f}%)')
by_src = {}
for w in all_words:
    by_src[w['zh_src']] = by_src.get(w['zh_src'], 0) + 1
print('来源:', by_src)

json.dump(all_words, open('med_zh_aligned.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved med_zh_aligned.json')
