# -*- coding: utf-8 -*-
"""中级三语词汇表 v4：
CN优先级: official(官方map) > zhocr(med_zh_read按日文对齐) > oldalign > added(补译)
"""
import json, sys, io, re
from collections import Counter
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

# ---- 官方 en->cn ----
cn_map = {}
for pno, en0, cn in pairs:
    n = norm_en(en0)
    if not n:
        continue
    if n not in cn_map:
        cn_map[n] = (len(en0), cn)
def find_official(en_txt):
    n = norm_en(en_txt)
    if n and n in cn_map:
        return cn_map[n][1]
    return None

# ---- zh_read 日文对齐 ----
zh_map = {}
zh_mainmap = {}
zh_full = []
for page, entries in zh.items():
    for (jp, cn) in entries:
        zh_full.append((jp, cn))
        for k in {norm(jp), norm(strip_bracket(jp)), norm(main_part(jp)), norm(jp.replace('-', ''))}:
            if k:
                zh_map.setdefault(k, (jp, cn))
        mp = norm(main_part(jp))
        if mp:
            zh_mainmap.setdefault(mp, []).append((jp, cn))
def find_zh(kanji):
    c = norm(kanji)
    for key in [c, norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))]:
        if key and key in zh_map:
            return zh_map[key]
    return None

# ---- override（官方无独立词条，补译）----
override = {
    'よさ': '好处，优点', 'グルメ': '美食', '簡易': '简易', 'なぜか': '不知为何',
    '名産': '名产', '最大': '最大', '中古': '二手', '学園': '学园', '早口': '语速快',
    'ほっぺたが落ちる': '好吃得不得了', 'いざ': '关键时刻；一旦',
    '～機関（国際機関': '～机构（国际机构）', '気楽さ': '轻松自在', '社会保障': '社会保障',
    'おむつ': '尿布', '日数': '天数', '未婚': '未婚', 'ポイント': '要点，重点',
    '印象的（な）': '令人印象深刻的', '熱気': '热情', 'エッセイ': '随笔，散文',
    'もの（ものの考え方': '事物（事物的想法）', '向き合う': '面对面，正视', 'プラスチック': '塑料',
    '驚き': '惊讶', '永久': '永久', '可能性': '可能性', '便利さ': '便利性',
    '上り下り-する': '上下（山）', '何の～もない（何の関係もない': '毫无～（毫无关系）',
    '国語[教科名': '国语', '野生': '野生', 'ファンクラブ': '粉丝俱乐部',
    '思い通り': '如自己所愿', '電源構成': '电源构成', '地熱': '地热', '過程': '过程',
    'バイオマス': '生物质', 'バブル景気': '泡沫经济', '数値': '数值', 'カカオ豆': '可可豆',
    '概要': '概要',
}

# ---- NE ----
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
    if k.count('（') > k.count('）'):
        k += '）'
    if k.count('(') > k.count(')'):
        k += ')'
    return k

rows = []
src_cnt = Counter()
problems = []
for k in sorted(en, key=int):
    for idx, (kanji, kana, etxt) in enumerate(en[k], 1):
        src = None
        cn = find_official(etxt)
        if cn:
            src = 'official'
        if not cn:
            hit = find_zh(kanji)
            if hit:
                cn = hit[1]; src = 'zhocr'
        if not cn:
            mp = main_part(kanji).strip()
            if mp in override:
                cn = override[mp]; src = 'added'
            elif kanji in override:
                cn = override[kanji]; src = 'added'
            else:
                # 模糊 sub：从 zh_full 找主词前缀匹配
                c3 = norm(main_part(kanji))
                if c3 and len(c3) >= 2:
                    for jp, cno in zh_full:
                        zmp = norm(main_part(jp))
                        if zmp and len(zmp) >= 2 and (zmp.startswith(c3) or c3.startswith(zmp)):
                            cn = cno; src = 'sub'
                            break
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
