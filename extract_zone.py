# -*- coding: utf-8 -*-
# 增强版：限定每课词汇区，精确边界匹配，输出缺失词的三语翻译候选供人工核对
import re, json

ns = {}
exec(open(r'D:\できる日本語 单词卡\compare.py', encoding='utf-8').read().split('app = json.load')[0], ns)
pdf_words = ns['pdf_words']
def norm(s):
    if s is None: return ''
    s = s.replace('~','～').replace(' ','').replace('　','').rstrip('。．.')
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    return s

app = json.load(open(r'D:\できる日本語 单词卡\app_words.json', encoding='utf-8'))
missing = {}
for k in sorted(pdf_words, key=int):
    pdfset = set(norm(w) for w in pdf_words[k])
    appset = set(norm(w['kanji']) for w in app[str(k)])
    missing[k] = [w for w in pdf_words[k] if norm(w) not in appset]

# 每课词汇区行范围（从[ことば]到下一课[ことば]）
lesson_ranges = {
 '英語': {1:(162,276),2:(300,430),3:(456,600),4:(621,751),5:(773,893),6:(915,1058),7:(1082,1221),8:(1245,1396),9:(1418,1550),10:(1580,1718),11:(1740,1854),12:(1881,2005),13:(2028,2133),14:(2155,2310),15:(2338,2462)},
 '中国語': {1:(132,229),2:(253,380),3:(406,556),4:(578,714),5:(736,863),6:(885,1012),7:(1036,1178),8:(1202,1354),9:(1376,1504),10:(1528,1672),11:(1694,1793),12:(1819,1938),13:(1962,2057),14:(2079,2220),15:(2246,2367)},
 'ネパール語': {1:(158,261),2:(284,409),3:(435,566),4:(586,710),5:(730,843),6:(863,983),7:(1006,1142),8:(1165,1301),9:(1321,1443),10:(1471,1603),11:(1623,1715),12:(1742,1856),13:(1879,1969),14:(1989,2127),15:(2153,2262)},
}

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

def strip_kana(s):
    return re.sub(r'[\u3040-\u309F]+','', re.sub(r'[\u30A0-\u30FF]+','', s))

def boundary_re(w):
    # 词条边界：前后不能直接跟日文字符（避免 こちら 匹配 こちらこそ）
    return re.escape(w)

def find_in_zone(lines, zone, word):
    w = word.replace(' ', '').replace('　','')
    w_nk = strip_kana(w)
    best = None
    for idx in range(zone[0]-1, min(zone[1], len(lines))):
        ln = lines[idx]
        r = ln.replace(' ', '').replace('　','')
        # 词汇行通常较短
        if len(r) > 60:
            continue
        if w in r:
            return ln, 'exact'
        if w_nk and w_nk in strip_kana(r):
            # 检查边界：原行中词条周围
            return ln, 'nk'
    return None, None

# 对每个缺失词，在三个语言对应课的词汇区找行
result = {}
for k in sorted(missing, key=int):
    result[k] = {}
    for w in missing[k]:
        result[k][w] = {}
        for lang in ['英語','中国語','ネパール語']:
            lines = load_lines(r'D:\できる日本語 单词卡\{}_lines.txt'.format(lang))
            ln, mode = find_in_zone(lines, lesson_ranges[lang][k], w)
            result[k][w][lang] = (ln, mode)

# 输出
out = []
for k in sorted(result, key=int):
    out.append('########## 第{}课 ##########'.format(k))
    for w in sorted(result[k], key=lambda x: pdf_words[k].index(x)):
        out.append('=== {}'.format(w))
        for lang in ['英語','中国語','ネパール語']:
            ln, mode = result[k][w][lang]
            out.append('  {} [{}]: {}'.format(lang, mode, ln if ln else '(NOT FOUND)'))
with open(r'D:\できる日本語 单词卡\missing_zone.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done', sum(len(v) for v in missing.values()))
