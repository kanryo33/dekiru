# -*- coding: utf-8 -*-
"""中级三语词汇表 v6：加入 236 词补译表"""
import json, sys, io, re
from collections import Counter
sys.path.insert(0, '.')
from med_miss_override import OVERRIDE
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))
zh = json.load(open('med_zh_read.json', encoding='utf-8'))
pairs = json.load(open('med_zh_en_cn_map.json', encoding='utf-8'))

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
def norm_en(s):
    s = s.lower()
    s = re.sub(r'[\u3040-\u30ff\u4e00-\u9fff\u3000-]', ' ', s)
    s = re.sub(r"[’']", ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

cn_map = {}
for pno, en0, cn in pairs:
    n = norm_en(en0)
    if not n: continue
    if n not in cn_map:
        cn_map[n] = (len(en0), cn)
def find_official(en_txt):
    n = norm_en(en_txt)
    if n and n in cn_map:
        return cn_map[n][1]
    n2 = re.sub(r'\[[^\]]*\]', '', en_txt)
    n2 = re.sub(r'\([^)]*\)', '', n2)
    n2 = norm_en(n2)
    if n2 and n2 in cn_map:
        return cn_map[n2][1]
    return None
def find_ensub(en_txt):
    toks = set(norm_en(en_txt).split())
    if len(toks) < 3: return None
    stop = {'to','the','a','an','of','and','in','on','for','with','at','by','from','up','down','out','off','into','as','is','are','be','it','its','that','this','one','you','here','there','they','their','or','so','very','much','more','most','not','no','do','does','can','will','would','should','all','any','some','etc','per'}
    core = toks - stop
    if len(core) < 2: return None
    best = None
    for n, (L, cn) in cn_map.items():
        nset = set(n.split())
        inter = core & nset
        if len(inter) >= 2 and (len(nset) <= len(core) + 2):
            score = len(inter) + 0.5 * min(len(nset), len(core)) / max(len(nset), len(core))
            if best is None or score > best[0]:
                best = (score, cn)
    return best[1] if best else None

zh_map = {}
zh_full = []
for page, entries in zh.items():
    for (jp, cn) in entries:
        zh_full.append((jp, cn))
        for k in {norm(jp), norm(strip_bracket(jp)), norm(main_part(jp)), norm(jp.replace('-', ''))}:
            if k:
                zh_map.setdefault(k, (jp, cn))
def find_zh(kanji, kana):
    for key in [norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', '')), norm(kana)]:
        if key and key in zh_map:
            return zh_map[key][1]
    c3 = norm(main_part(kanji))
    if c3 and len(c3) >= 2:
        for jp, cno in zh_full:
            zmp = norm(main_part(jp))
            if zmp and len(zmp) >= 2 and (zmp.startswith(c3) or c3.startswith(zmp)) and len(zmp) - len(c3) <= 3:
                return cno
    return None

ne_map = {}
for k, items in ne.items():
    for (kanji, kana, netxt) in items:
        for kk in {norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))}:
            if kk:
                ne_map.setdefault(kk, netxt)
def find_ne(kanji):
    for kk in [norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))]:
        if kk and kk in ne_map:
            return ne_map[kk]
    return ''

def fix_kanji(kanji):
    k = re.sub(r'\[.*?\]', '', kanji)
    if k.count('（') > k.count('）'): k += '）'
    if k.count('(') > k.count(')'): k += ')'
    return k

rows = []
src_cnt = Counter()
problems = []
for k in sorted(en, key=int):
    for idx, (kanji, kana, etxt) in enumerate(en[k], 1):
        cn = src = None
        cn = find_official(etxt)
        if cn: src = 'official'
        if not cn:
            if kanji in OVERRIDE:
                cn, src = OVERRIDE[kanji], 'added'
            elif main_part(kanji).strip() in OVERRIDE:
                cn, src = OVERRIDE[main_part(kanji).strip()], 'added'
        if not cn:
            c = find_zh(kanji, kana)
            if c:
                cn, src = c, 'zhocr'
        if not cn:
            c = find_ensub(etxt)
            if c:
                cn, src = c, 'ensub'
        if not cn:
            src = 'miss'
            problems.append((k, kanji, etxt))
        src_cnt[src] += 1
        rows.append({
            'lesson': int(k), 'no': idx, 'kanji': fix_kanji(kanji), 'kana': kana,
            'en': etxt, 'cn': cn if cn else '', 'ne': find_ne(kanji), 'src': src
        })

print('来源统计:', dict(src_cnt))
print('仍缺中文:', len(problems))
for p in problems:
    print(' ', p)
json.dump(rows, open('med_trilingual.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入 med_trilingual.json, 总词条:', len(rows))
