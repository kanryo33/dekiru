# -*- coding: utf-8 -*-
# 自动为缺失词条从三语行文本提取翻译（含假名清理），先输出供核对
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 官方词表（来自 compare.py）
ns = {}
exec(open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read().split('app = json.load')[0], ns)
pdf_words = ns['pdf_words']
def norm(s):
    if s is None: return ''
    s = s.replace('~','～').replace(' ','').replace('　','').rstrip('。．.')
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    return s

app = json.load(open(r'D:\できる日本語 单词卡\app_words.json', encoding='utf-8'))
app_by_norm = {}
for k, entries in app.items():
    for e in entries:
        app_by_norm[norm(e['kanji'])] = e

# 每课缺失词条
missing = {}
for k in sorted(pdf_words, key=int):
    pdfset = set(norm(w) for w in pdf_words[k])
    appset = set(norm(w['kanji']) for w in app[str(k)])
    missing[k] = [w for w in pdf_words[k] if norm(w) not in appset]

# 读取三语行文本（只读词汇区，跳过每课标题等）
def load_lines(path):
    lines = []
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('==== PAGE'):
            continue
        # 去掉列前缀 L/R
        if ln[:1] in ('L','R') and len(ln) > 2 and ln[1] == ' ':
            ln = ln[2:]
        lines.append(ln)
    return lines

en_lines = load_lines(r'D:\できる日本語 单词卡\英語_lines.txt')
cn_lines = load_lines(r'D:\できる日本語 单词卡\中国語_lines.txt')
ne_lines = load_lines(r'D:\できる日本語 单词卡\ネパール語_lines.txt')

HIRA = re.compile(r'[\u3040-\u309F]+')
KATA = re.compile(r'[\u30A0-\u30FF]+')
def strip_kana(s):
    s = HIRA.sub('', s)
    s = KATA.sub('', s)
    return s

def find_translation(lines, word, lesson):
    # 候选：行去除假名后包含 word 核心
    core = norm(word)
    # 处理特殊形式
    cands = []
    for ln in lines:
        t = strip_kana(ln)
        # 精确包含
        if core and core in t.replace(' ', ''):
            cands.append(ln)
    return cands

# 测试第1课缺失词
out = []
for w in missing[1]:
    out.append('### ' + w)
    for lang, lines in [('EN', en_lines), ('CN', cn_lines), ('NE', ne_lines)]:
        cands = find_translation(lines, w, 1)
        if cands:
            out.append(' {} => {}'.format(lang, cands[:3]))
        else:
            out.append(' {} => (none)'.format(lang))
with open(r'D:\できる日本語 单词卡\auto_test_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
