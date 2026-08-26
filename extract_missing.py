# -*- coding: utf-8 -*-
# 改进版：为官方词表中程序缺失的词条，从三语PDF行文本提取翻译
# 输出结构化结果供人工核对
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ns = {}
exec(open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read().split('app = json.load')[0], ns)
pdf_words = ns['pdf_words']
def norm(s):
    if s is None: return ''
    s = s.replace('~','～').replace(' ','').replace('　','').rstrip('。．.')
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    return s

app = json.load(open(r'D:\できる日本語 单词卡\app_words.json', encoding='utf-8'))

# 每课缺失词条
missing = {}
for k in sorted(pdf_words, key=int):
    pdfset = set(norm(w) for w in pdf_words[k])
    appset = set(norm(w['kanji']) for w in app[str(k)])
    missing[k] = [w for w in pdf_words[k] if norm(w) not in appset]

def load_lines(path):
    lines = []
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('==== PAGE'):
            continue
        if ln[:1] in ('L','R') and len(ln) > 2 and ln[1] == ' ':
            ln = ln[2:]
        lines.append(ln)
    return lines

en_lines = load_lines(r'D:\できる日本語 单词卡\英語_lines.txt')
cn_lines = load_lines(r'D:\できる日本語 单词卡\中国語_lines.txt')
ne_lines = load_lines(r'D:\できる日本語 单词卡\ネパール語_lines.txt')

HIRA = re.compile(r'[\u3040-\u309F]+')
KATA = re.compile(r'[\u30A0-\u30FF]+')
DEV = re.compile(r'[\u0900-\u097F]+')
def has_kana(s): return bool(HIRA.search(s) or KATA.search(s))
def strip_kana(s): return HIRA.sub('', KATA.sub('', s))

def extract_translation(line, word):
    """给定一行(可能含假名标注+词条+翻译)，尽力返回翻译部分。失败返回None"""
    raw = line.replace(' ', '').replace('　', '')
    w = word.replace(' ', '').replace('　', '')
    # 情况1：词条原文（含假名）直接在raw中
    if w in raw:
        rest = raw.replace(w, '', 1)
    else:
        # 情况2：词条核心（去假名）在"行去假名"中
        raw_nk = strip_kana(raw)
        w_nk = strip_kana(w)
        if w_nk and w_nk in raw_nk:
            # 从raw中移除词条：需要找到w_nk在raw_nk的位置，映射回raw较复杂，改用raw_nk
            rest = raw_nk.replace(w_nk, '', 1)
        else:
            return None
    # 清理残余日语假名标注
    rest = rest.strip()
    return rest

def find_line(lines, word):
    raw_lines = [l.replace(' ', '').replace('　','') for l in lines]
    w = word.replace(' ', '').replace('　','')
    w_nk = strip_kana(w)
    for i, r in enumerate(raw_lines):
        if w in r:
            return lines[i]
    if w_nk:
        for i, r in enumerate(raw_lines):
            r_nk = strip_kana(r)
            if w_nk and w_nk in r_nk:
                return lines[i]
    return None

out = []
for k in sorted(missing, key=int):
    if not missing[k]:
        continue
    out.append('########## 第{}课 缺失词翻译提取 ##########'.format(k))
    for w in missing[k]:
        out.append('=== {}'.format(w))
        for lang, lines in [('EN', en_lines), ('CN', cn_lines), ('NE', ne_lines)]:
            ln = find_line(lines, w)
            if ln is None:
                out.append('  {}: (NOT FOUND)'.format(lang))
                continue
            tr = extract_translation(ln, w)
            out.append('  {}: [line] {}'.format(lang, ln))
            out.append('  {}: [trans] {}'.format(lang, tr if tr else '(EMPTY)'))

with open(r'D:\できる日本語 单词卡\missing_translations_raw.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written')
