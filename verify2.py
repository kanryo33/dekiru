# -*- coding: utf-8 -*-
import re, json, sys, io, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
html = open(r'D:\できる日本語 单词卡\index.html', encoding='utf-8').read()
m = re.search(r'const lessonWordData = \{(.*?)\n\};', html, re.S)
body = m.group(1)
pat = re.compile(r'\{"kanji":(".*?"),"kana":(".*?"),"eng":(".*?"),"cn":(".*?"),"ne":(".*?")\}', re.S)
blocks = re.split(r'\n\s*(\d+): \[', body)

spec = importlib.util.spec_from_file_location('mt', r'D:\できる日本語 单词卡\missing_translations.py')
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)
missing_data = mt.missing_data

empty = []
for k, d in missing_data.items():
    for w, (kana, eng, cn, ne) in d.items():
        if not eng or not cn or not ne:
            empty.append((k, w, 'eng' if not eng else 'cn' if not cn else 'ne'))
print('缺失词条中空字段数:', len(empty))
for e in empty:
    print(e)

all_words = 0
no_eng = []
for i in range(1, len(blocks), 2):
    for mm in pat.finditer(blocks[i+1]):
        all_words += 1
        vals = [json.loads(mm.group(j)) for j in range(1,6)]
        if not vals[2] or not vals[3] or not vals[4]:
            no_eng.append((blocks[i], vals[0]))
print('总词条数:', all_words, '| 缺 eng/cn/ne 的词条:', len(no_eng))
for e in no_eng[:20]:
    print(e)
