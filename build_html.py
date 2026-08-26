# -*- coding: utf-8 -*-
import re, json, sys, io, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. 提取官方词表 pdf_words
src = open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read()
start = src.find('pdf_words = {')
end = src.find('# 载入程序词汇')
ns = {}
exec(src[start:end], ns)
pdf_words = ns['pdf_words']

# 2. 程序已有词
app = json.load(open(r'D:\できる日本語 单词卡\app_words.json', encoding='utf-8'))

# 3. 缺失词翻译
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

# 4. 假名数据修正（程序已有词的错误假名）
KANA_FIX = {
    (4, '東'): 'ひがし',
    (12, '歯'): 'は',
    (15, 'かかります'): 'かかります',
}

# 5. 组装每课词表
lesson_data = {}
unresolved = []
for k in sorted(pdf_words, key=int):
    arr = []
    app_by_norm = {}
    for w in app.get(str(k), []):
        app_by_norm.setdefault(norm(w['kanji']), w)
    for orig in pdf_words[k]:
        w = app_by_norm.get(norm(orig))
        if w is not None:
            kanji = orig
            kana = w['kana']
            # 应用假名修正
            if (int(k), orig) in KANA_FIX:
                kana = KANA_FIX[(int(k), orig)]
            eng, cn, ne = w['eng'], w['cn'], w['ne']
        else:
            md = missing_data.get(int(k), {}).get(orig)
            if md is None:
                unresolved.append((k, orig))
                continue
            kana, eng, cn, ne = md
            kanji = orig
        arr.append({"kanji": kanji, "kana": kana, "eng": eng, "cn": cn, "ne": ne})
    lesson_data[int(k)] = arr

print('未解决词条数:', len(unresolved))
for k, w in unresolved:
    print('  [第{}课] {}'.format(k, w))

# 6. 生成 JS 并替换 index.html
js_parts = []
for k in sorted(lesson_data, key=int):
    items = []
    for o in lesson_data[k]:
        items.append('{' + ','.join('"{}":{}'.format(f, json.dumps(o[f], ensure_ascii=False)) for f in ['kanji','kana','eng','cn','ne']) + '}')
    js_parts.append('  {}: [\n    {}\n  ]'.format(k, ',\n    '.join(items)))
js_block = 'const lessonWordData = {\n' + ',\n'.join(js_parts) + '\n};'

html_path = r'D:\できる日本語 单词卡\index.html'
html = open(html_path, encoding='utf-8').read()
m = re.search(r'const lessonWordData = \{.*?\n\};', html, re.S)
if not m:
    print('ERROR: lessonWordData not found')
    sys.exit(1)
new_html = html[:m.start()] + js_block + html[m.end():]

# 7. 备份原文件并写回
open(html_path + '.bak', 'w', encoding='utf-8').write(html)
open(html_path, 'w', encoding='utf-8').write(new_html)

# 8. 输出统计
total = sum(len(v) for v in lesson_data.values())
print('重建完成: 总词条数 =', total)
for k in sorted(lesson_data, key=int):
    print('第{}课: {}词条'.format(k, len(lesson_data[k])))
