# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = open(r'D:\できる日本語 单词卡\chuukyuu_英語_lines.txt', encoding='utf-8').read().split('\n')

JP_RE = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
KANA_RE = re.compile(r'[\u3040-\u30ff]')
KATAKANA_RE = re.compile(r'[\u30a0-\u30ff]')

def strip_marker(ln):
    ln = ln.strip()
    if ln.startswith('L '): ln = ln[2:]
    elif ln.startswith('R '): ln = ln[2:]
    if ' | ' in ln:
        parts = ln.split(' | ')
        left = parts[0]
        right = ' '.join(parts[1:])
        return left, right
    return ln, ''

def is_jp(s):
    return bool(JP_RE.search(s))

def is_kana(s):
    return bool(KANA_RE.search(s))

def has_kanji(s):
    return bool(re.search(r'[\u4e00-\u9fff]', s))

def extract_jp(s):
    """提取日文部分：保留汉字与假名，去掉注音间的空格、括号注记合并"""
    # 按 token 拆分
    tokens = s.split()
    jp_tokens = []
    en_tokens = []
    for t in tokens:
        if is_jp(t):
            jp_tokens.append(t)
        else:
            en_tokens.append(t)
    return ' '.join(jp_tokens), ' '.join(en_tokens)

# 第1课词汇区 156-315
zone = en[155:315]
skip_pat = re.compile(r'^(［ことば］|話 読 聞 書|もう一 度 聞 こう|第\d+課|==== PAGE)')
topic_pat = re.compile(r'^\d+　')

current = None
entries = []
for ln in zone:
    if skip_pat.search(ln.strip()):
        continue
    left, right = strip_marker(ln)
    if not left and not right:
        continue
    # 合并左右
    full = (left + ' ' + right).strip()
    if not full:
        continue
    # 跳过スモールトピック标题（如 1　アルバイトを探す）及其说明
    if topic_pat.match(full):
        continue
    if is_jp(full):
        # 词条或注音或长句
        jp_part, en_part = extract_jp(full)
        if en_part and jp_part:
            # 词条+翻译同行
            entries.append((jp_part, en_part))
        else:
            # 只有日文：注音行/汉字行/长句
            entries.append((jp_part, ''))
    else:
        # 纯英文：翻译行（可能是上一词条的翻译跨行）
        if entries and entries[-1][1] == '':
            entries[-1] = (entries[-1][0], full)
        else:
            entries.append(('', full))

for e in entries:
    print(repr(e[0]), '=>', repr(e[1]))
