# -*- coding: utf-8 -*-
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 提取官方词表
src = open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read()
start = src.find('pdf_words = {')
end = src.find('# 载入程序词汇')
ns = {}
exec(src[start:end], ns)
pdf_words = ns['pdf_words']

def norm(s):
    if s is None: return ''
    s = s.replace('~','～').replace(' ','').replace('　','')
    s = s.rstrip('。．.')
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    return s

# 解析重建后的 index.html lessonWordData
html = open(r'D:\できる日本語 单词卡\index.html', encoding='utf-8').read()
m = re.search(r'const lessonWordData = \{(.*?)\n\};', html, re.S)
body = m.group(1)
# 解析每课
# 用正则提取 {kanji:"...",kana:"...",eng:"...",cn:"...",ne:"..."}
pat = re.compile(r'\{"kanji":(".*?"),"kana":(".*?"),"eng":(".*?"),"cn":(".*?"),"ne":(".*?")\}', re.S)
# 按课拆分
lesson_blocks = re.split(r'\n\s*(\d+): \[', body)
# lesson_blocks[0] 是前缀，之后是 (课号, 内容) 交替
new_app = {}
for i in range(1, len(lesson_blocks), 2):
    k = int(lesson_blocks[i])
    items = []
    for m2 in pat.finditer(lesson_blocks[i+1]):
        def unq(s):
            return json.loads(s)
        items.append({f: unq(m2.group(j)) for f, j in [('kanji',1),('kana',2),('eng',3),('cn',4),('ne',5)]})
    new_app[str(k)] = items

# 校验
total_pdf = 0
total_new = 0
all_missing = 0
all_extra = 0
for k in sorted(pdf_words, key=int):
    pdfset = set(norm(w) for w in pdf_words[k])
    appset = set(norm(w['kanji']) for w in new_app[str(k)])
    missing = pdfset - appset
    extra = appset - pdfset
    all_missing += len(missing)
    all_extra += len(extra)
    total_pdf += len(pdfset)
    total_new += len(new_app[str(k)])
    if missing or extra:
        print('第{}课 缺失={} 独有={}'.format(k, sorted(missing), sorted(extra)))
print('官方去重词条总数:', total_pdf)
print('重建后词条总数:', total_new)
print('缺失总计:', all_missing, '| 独有总计:', all_extra)

# 检查假名修正是否生效
for k in ['4','12','15']:
    for w in new_app[k]:
        if w['kanji'] == '東':
            print('L4 東 kana =', w['kana'])
        if w['kanji'] == '歯':
            print('L12 歯 kana =', w['kana'])
        if w['kanji'] == 'かかります':
            print('L15 かかります kana =', w['kana'])

# 抽样显示每课前3条确认格式
for k in ['1','5','14']:
    print('--- 第{}课 抽样 ---'.format(k))
    for w in new_app[k][:3]:
        print(w)
