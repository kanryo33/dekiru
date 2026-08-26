# -*- coding: utf-8 -*-
"""中级三语词汇表最终版：
骨架 = med_words_en(第2版官方英文)
NE   = med_words_ne(第2版官方尼语)
CN   = med_zh_read(旧版官方中文) 对齐 + 补译override
"""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))
zh = json.load(open('med_zh_read.json', encoding='utf-8'))

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

# ---- 中文查找表 ----
zh_map = {}
zh_mainmap = {}
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

def find_zh(kanji, kana):
    c = norm(kanji)
    if c in zh_map: return zh_map[c], 'exact'
    c2 = norm(strip_bracket(kanji))
    if c2 and c2 in zh_map: return zh_map[c2], 'strip'
    c3 = norm(main_part(kanji))
    if c3 and c3 in zh_map: return zh_map[c3], 'main'
    c4 = norm(kanji.replace('-', ''))
    if c4 and c4 in zh_map: return zh_map[c4], 'nodash'
    if c3 and c3 in zh_mainmap: return zh_mainmap[c3][0], 'mainmap'
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

# ---- 补译 override（官方旧版中文无此独立词条）----
override = {
    'よさ': '好处，优点',
    'グルメ': '美食',
    '簡易': '简易',
    'なぜか': '不知为何',
    '名産': '名产',
    '最大': '最大',
    '中古': '二手',
    '学園': '学园',
    '早口': '语速快',
    'ほっぺたが落ちる': '好吃得不得了',
    'いざ': '关键时刻；一旦',
    '～機関（国際機関': '～机构（国际机构）',
    '気楽さ': '轻松自在',
    '社会保障': '社会保障',
    'おむつ': '尿布',
    '日数': '天数',
    '未婚': '未婚',
    'ポイント': '要点，重点',
    '印象的（な）': '令人印象深刻的',
    '熱気': '热情',
    'エッセイ': '随笔，散文',
    'もの（ものの考え方': '事物（事物的想法）',
    '向き合う': '面对面，正视',
    'プラスチック': '塑料',
    '驚き': '惊讶',
    '永久': '永久',
    '可能性': '可能性',
    '便利さ': '便利性',
    '上り下り-する': '上下（山）',
    '何の～もない（何の関係もない': '毫无～（毫无关系）',
    '国語[教科名': '国语',
    '野生': '野生',
    'ファンクラブ': '粉丝俱乐部',
    '思い通り': '如自己所愿',
    '電源構成': '电源构成',
    '地熱': '地热',
    '過程': '过程',
    'バイオマス': '生物质',
    'バブル景気': '泡沫经济',
    '数値': '数值',
    'カカオ豆': '可可豆',
    '概要': '概要',
}

# ---- kanji 完整形式修正：优先用 zh_read 完整形式 ----
def fix_kanji(kanji, lesson, zhjp):
    k = kanji
    # 去掉 [xxx] 方括号标记
    k = re.sub(r'\[.*?\]', '', k)
    # 若 zh 匹配到完整形式且 en 括号未闭合，尝试用 zh 完整形式
    if zhjp and (k.count('（') != k.count('）')):
        # zh 完整形式
        if zhjp.count('（') == zhjp.count('）') and main_part(k) == main_part(zhjp):
            return zhjp
        # 简单补右括号
        k = k.replace('（', '（').replace('）', '）')
        if k.count('（') > k.count('）'):
            k += '）'
        if k.count('(') > k.count(')'):
            k += ')'
        return k
    return k

rows = []
from collections import Counter
src_cnt = Counter()
zh_problems = []
for k in sorted(en, key=int):
    for idx, (kanji, kana, etxt) in enumerate(en[k], 1):
        found = find_zh(kanji, kana)
        if found and found[0]:
            (zhjp, zh_txt), src = found
        else:
            zhjp, zh_txt, src = None, '', None
        # override 优先
        if zh_txt and zh_txt in override.values() and src == 'sub':
            pass  # sub 匹配可疑的用 override
        # 修正 sub 误配：若 en 主词在 override 中，用 override
        if not zh_txt or src in ('sub',):
            mp = main_part(kanji).strip()
            if mp in override:
                zh_txt = override[mp]
                src = 'added'
            elif kanji in override:
                zh_txt = override[kanji]
                src = 'added'
        if not zh_txt:
            if kanji in override:
                zh_txt = override[kanji]; src = 'added'
            else:
                src = 'miss'
                zh_problems.append((k, kanji, etxt))
        if src:
            src_cnt[src] += 1
        clean_kanji = fix_kanji(kanji, k, zhjp)
        rows.append({
            'lesson': int(k), 'no': idx, 'kanji': clean_kanji, 'kana': kana,
            'en': etxt, 'cn': zh_txt, 'ne': find_ne(kanji), 'src': src
        })

print('来源统计:', dict(src_cnt))
print('仍缺中文:', len(zh_problems))
for p in zh_problems:
    print(' ', p)
json.dump(rows, open('med_trilingual.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入 med_trilingual.json, 总词条:', len(rows))
