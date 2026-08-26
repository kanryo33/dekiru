# -*- coding: utf-8 -*-
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 从 compare.py 提取 pdf_words
src = open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read()
start = src.find('pdf_words = {')
end = src.find('# 载入程序词汇')
pdf_src = src[start:end]
ns = {}
exec(pdf_src, ns)
pdf_words = ns['pdf_words']

# 载入翻译数据
import importlib.util
spec = importlib.util.spec_from_file_location("missing_translations", r'D:\できる日本語 单词卡\missing_translations.py')
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)
missing_data = mt.missing_data

def norm(s):
    if s is None: return ''
    s = s.replace('~','～').replace(' ','').replace('　','')
    s = s.rstrip('。．.')
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    return s

app = json.load(open(r'D:\できる日本語 单词卡\app_words.json', encoding='utf-8'))

total_missing = 0
uncovered = []
extra_keys = []
for k in sorted(pdf_words, key=int):
    pdfset = set(norm(w) for w in pdf_words[k])
    appset = set(norm(w['kanji']) for w in app[str(k)])
    missing_norm = pdfset - appset
    # 找出官方原文里 norm 后属于 missing 的词条
    missing_orig = [w for w in pdf_words[k] if norm(w) in missing_norm]
    total_missing += len(missing_orig)
    # missing_data 是否有该课、该词条
    md = missing_data.get(int(k), {})
    for w in missing_orig:
        if w not in md:
            uncovered.append((k, w))
    # missing_data 多余 key 检查
    for key in md:
        if key not in pdf_words[k]:
            extra_keys.append((k, key))
    print('第{}课: 官方词条数={} 缺失词条数={} 已备翻译={}'.format(
        k, len(set(norm(w) for w in pdf_words[k])), len(missing_orig), len(missing_orig) - sum(1 for w in missing_orig if w not in md)))

print('\n总缺失词条数:', total_missing)
print('缺翻译的词条:', len(uncovered))
for k, w in uncovered:
    print('  [第{}课] {}'.format(k, w))
print('\nmissing_data 中多余的 key:', len(extra_keys))
for k, key in extra_keys:
    print('  [第{}课] {}'.format(k, key))
