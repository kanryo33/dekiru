# -*- coding: utf-8 -*-
"""中级三语词汇表组装 v2：更严格匹配，记录来源"""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))
zh = json.load(open('med_zh_read.json', encoding='utf-8'))
al = json.load(open('med_zh_aligned.json', encoding='utf-8'))

def norm(s):
    if not s: return ''
    s = s.replace(' ', '').replace('\u3000', '').replace('〜', '～')
    for a, b in zip('０１２３４５６７８９', '0123456789'):
        s = s.replace(a, b)
    return s

def strip_bracket(s):
    # 正确去括号（处理未闭合）
    return re.sub(r'[（(].*?[）)]', '', s)

def main_part(s):
    # 括号前主词
    m = re.split(r'[（(]', s)
    return m[0].strip()

def has_kana(s):
    return any('\u3040' <= c <= '\u30ff' for c in s)

# ---- 中文查找表 ----
zh_map = {}      # key -> (jp, cn)
zh_mainmap = {}  # 主词 -> [(jp, cn)]
zh_kana = {}     # kana(括号内) -> [(jp, cn)]
zh_full = []
for page, entries in zh.items():
    for (jp, cn) in entries:
        zh_full.append((jp, cn))
        keys = {norm(jp), norm(strip_bracket(jp)), norm(main_part(jp)), norm(jp.replace('-', ''))}
        for k in keys:
            if k:
                zh_map.setdefault(k, (jp, cn))
        mp = norm(main_part(jp))
        if mp:
            zh_mainmap.setdefault(mp, []).append((jp, cn))
        for km in re.findall(r'[（(]([ぁ-んァ-ヶー・]+)[）)]', jp):
            zh_kana.setdefault(norm(km), []).append((jp, cn))

def find_zh(kanji, kana):
    c = norm(kanji)
    # 1. 完整精确
    if c in zh_map:
        return zh_map[c], 'exact'
    # 2. 去括号
    c2 = norm(strip_bracket(kanji))
    if c2 and c2 in zh_map:
        return zh_map[c2], 'strip'
    # 3. 主词
    c3 = norm(main_part(kanji))
    if c3 and c3 in zh_map:
        return zh_map[c3], 'main'
    # 4. 去'-'
    c4 = norm(kanji.replace('-', ''))
    if c4 and c4 in zh_map:
        return zh_map[c4], 'nodash'
    # 5. kana（括号内かな匹配）
    k = norm(kana)
    if k and k in zh_kana:
        return zh_kana[k][0], 'kana'
    # 6. 主词精确（en主词 in zh主词集）
    if c3 and c3 in zh_mainmap:
        return zh_mainmap[c3][0], 'mainmap'
    # 7. 子串：en主词是zh主词的前缀，或zh主词以en主词开头（长度>=2）
    if c3 and len(c3) >= 2:
        for jp, cn in zh_full:
            zmp = norm(main_part(jp))
            if not zmp or len(zmp) < 2:
                continue
            if zmp == c3 or zmp.startswith(c3) or c3.startswith(zmp):
                return (jp, cn), 'sub'
    return None, None

# ---- NE 查找 ----
ne_map = {}
for k, items in ne.items():
    for (kanji, kana, netxt) in items:
        keys = {norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))}
        for kk in keys:
            if kk:
                ne_map.setdefault(kk, netxt)
def find_ne(kanji):
    for kk in [norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))]:
        if kk and kk in ne_map:
            return ne_map[kk]
    return ''

# 旧对齐（en_norm -> zh）
al_zh = {}
for x in al:
    if x.get('zh'):
        al_zh.setdefault(norm(x.get('en', '')), x['zh'])

rows = []
from collections import Counter
src_cnt = Counter()
for k in sorted(en, key=int):
    for idx, (kanji, kana, etxt) in enumerate(en[k], 1):
        found = find_zh(kanji, kana)
        jp, zh_txt, src = (found[0][0], found[0][1], found[1]) if found and found[0] else (None, '', None)
        if zh_txt:
            src_cnt[src] += 1
        else:
            en_n = norm(etxt)
            if en_n in al_zh:
                zh_txt = al_zh[en_n]; src = 'oldalign'
                src_cnt[src] += 1
            else:
                zh_txt = ''; src = 'miss'
                src_cnt[src] += 1
        rows.append({
            'lesson': int(k), 'no': idx, 'kanji': kanji, 'kana': kana,
            'en': etxt, 'cn': zh_txt, 'ne': find_ne(kanji), 'src': src
        })

print('匹配来源:', dict(src_cnt))
print('无中文:', sum(1 for r in rows if not r['cn']), '/ 无尼语:', sum(1 for r in rows if not r['ne']))
json.dump(rows, open('med_trilingual.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入 med_trilingual.json')
print('=== 无中文词条 ===')
for r in rows:
    if not r['cn']:
        print('课%d %s | %s | NE:%s' % (r['lesson'], r['kanji'], r['en'], r['ne']))
print('=== sub 匹配抽查（前30） ===')
n = 0
for r in rows:
    if r['src'] == 'sub':
        print('课%d %s | %s -> CN:%s' % (r['lesson'], r['kanji'], r['en'][:25], r['cn'][:20]))
        n += 1
        if n >= 30: break
