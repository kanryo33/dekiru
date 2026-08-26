# -*- coding: utf-8 -*-
import pymupdf, sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def segment(tokens, gap=25):
    if not tokens: return []
    tokens = sorted(tokens)
    segs = []
    cur = [tokens[0]]
    cur_x0 = tokens[0][0]
    for i in range(1, len(tokens)):
        if tokens[i][0] - tokens[i-1][1] > gap:
            segs.append((cur, cur_x0))
            cur = [tokens[i]]
            cur_x0 = tokens[i][0]
        else:
            cur.append(tokens[i])
    segs.append((cur, cur_x0))
    return [(' '.join(t[2] for t in toklist), x0) for toklist, x0 in segs]

# 判定是否"正常可读字符"（过滤乱码：Private Use / 无关符号）
def is_readable(s):
    # 保留 CJK 中文、拉丁、常用符号、数字
    for ch in s:
        o = ord(ch)
        if o >= 0xE000 and o <= 0xF8FF:  # PUA
            return False
        if o >= 0x1D00 and o <= 0x1DBF:  # 音标扩展
            return False
    return True

base = r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト'

# 英语：左右栏分开
path = os.path.join(base, '英語.pdf')
L, R = [], []
with pymupdf.open(path) as doc:
    for pno, page in enumerate(doc, start=1):
        words = page.get_text('words', sort=True)
        rows = {}
        for w in words:
            x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
            key = round(y0 / 3.0)
            rows.setdefault(key, []).append((x0, x1, txt))
        for key in sorted(rows):
            left_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 < 300]
            right_toks = [(x0,x1,t) for x0,x1,t in rows[key] if x0 >= 300]
            for seg, x0 in segment(left_toks):
                L.append(f'{pno}: {seg}')
            for seg, x0 in segment(right_toks):
                R.append(f'{pno}: {seg}')
print('=== 英语 左栏 第1课词汇区(从 知って楽しむ 开始) ===')
start = next(i for i,l in enumerate(L) if '知 っ て楽 し む' in l.replace(' ','') or '知って楽しむ' in l)
for l in L[start:start+40]:
    print(l)
print()
print('=== 英语 右栏 对应段 ===')
# 找右栏同一区域的起点：財産
startR = next(i for i,l in enumerate(R) if '財 産' in l.replace(' ','') or '財産' in l)
for l in R[startR:startR+40]:
    print(l)
