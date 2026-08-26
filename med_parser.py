# -*- coding: utf-8 -*-
import pymupdf, sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 字符判定
def is_jp_char(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30FF  # 假名
            or 0x3400 <= o <= 0x9FFF  # CJK
            or 0xF900 <= o <= 0xFAFF)  # CJK兼容

def has_jp(s):
    return any(is_jp_char(c) for c in s)

def is_pure_kana(s):
    s2 = s.replace(' ', '').replace('　','')
    if not s2: return False
    return all(0x3040 <= ord(c) <= 0x30FF or c in 'ー・、。' for c in s2)

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'
path = os.path.join(base, '英語.pdf')

def parse_page(page, side):
    """解析一页的一栏，返回词条列表 [(kanji, kana, eng)]"""
    words = page.get_text('words', sort=True)
    # 分栏
    if side == 'L':
        toks = [w for w in words if w[0] < 300]
        jp_xmax = 150
    else:
        toks = [w for w in words if w[0] >= 300]
        jp_xmax = 680
    if not toks: return []
    # 按 y 排序
    toks.sort(key=lambda w: (round(w[1],1), w[0]))
    # 逐 token 分类：日语词 token（x<jp_xmax） vs 翻译 token（x>=jp_xmax）
    entries = []  # 每个 {y0, y1, jp_tokens, eng_tokens}
    cur = None
    for w in toks:
        x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
        is_jp_pos = x0 < jp_xmax
        if cur is not None and y0 - cur['y1'] > 8:
            # 距离上一个词条太远 → 结束当前，开新
            cur = None
        if cur is None:
            cur = {'y0': y0, 'y1': y1, 'jp': [], 'eng': []}
            entries.append(cur)
        cur['y1'] = max(cur['y1'], y1)
        cur['y0'] = min(cur['y0'], y0)
        if is_jp_pos and has_jp(txt):
            cur['jp'].append((y0, x0, txt))
        else:
            cur['eng'].append((y0, x0, txt))
    return entries

with pymupdf.open(path) as doc:
    page = doc[3]
    for side in ['L', 'R']:
        entries = parse_page(page, side)
        print(f'===== {side}栏 第4页 词条数={len(entries)} =====')
        for e in entries:
            jp_txt = ' '.join(t[2] for t in sorted(e['jp'], key=lambda t:(t[0],t[1])))
            eng_txt = ' '.join(t[2] for t in sorted(e['eng'], key=lambda t:(t[0],t[1])))
            print(f'  [{jp_txt}]  <-  [{eng_txt}]')
