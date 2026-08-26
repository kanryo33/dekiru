# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = open(r'D:\できる日本語 单词卡\chuukyuu_英語_lines.txt', encoding='utf-8').read().split('\n')
cn = open(r'D:\できる日本語 单词卡\chuukyuu_中国語_lines.txt', encoding='utf-8').read().split('\n')
ne = open(r'D:\できる日本語 单词卡\chuukyuu_ネパール語_lines.txt', encoding='utf-8').read().split('\n')

# 英语版 ［ことば］ 起点
en_koto = [156,316,483,670,840,1023,1157,1337,1460,1633,1819,1956,2127,2265,2528]
cn_koto = [137,270,421,572,721,872,1008,1155,1256,1456,1613,1730,1884,1985,2173]
ne_koto = [141,265,414,578,715,868,1002,1143,1222,1399,1561,1677,1822,1920,2100]

lesson_titles = ['新しい一歩','楽しいショッピング','私の目標','住んでいる町で','大変な1日','旅行に行こう',
                 '西川さんの家へ','ありがとう','アルバイト先で','旅行に行って','地域社会の中で','私の健康法',
                 '親の気持ち・子の気持ち','イベント・行事','気になるニュース']

def count_jp_words(lines, start, end):
    """在词汇区内统计含日文字符的行数（词条+注音+翻译混合的粗指标）"""
    cnt = 0
    for i in range(start-1, end):
        ln = lines[i]
        # 跳过页脚/页码/标记行
        if '==== PAGE' in ln or 'できる日本語' in ln:
            continue
        if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', ln):
            cnt += 1
    return cnt

print('=== 《できる日本語 初中級 本冊【第2版】》 三語語彙リスト 識別総覧 ===')
print('（英語版 34頁 / 中国語版 32頁 / ネパール語版 32頁、2025/02/20）\n')
print('{:>3} {:<6} {:<14} {:>6} {:>6} {:>6} {:>8} {:>8} {:>8}'.format(
    '課','','課名','英词条','中行数','尼行数','英区間','中区間','尼区間'))
for idx in range(15):
    k = idx+1
    en_s, en_e = en_koto[idx], (en_koto[idx+1]-1 if idx<14 else len(en))
    cn_s, cn_e = cn_koto[idx], (cn_koto[idx+1]-1 if idx<14 else len(cn))
    ne_s, ne_e = ne_koto[idx], (ne_koto[idx+1]-1 if idx<14 else len(ne))
    ec = count_jp_words(en, en_s, en_e)
    cc = count_jp_words(cn, cn_s, cn_e)
    nc = count_jp_words(ne, ne_s, ne_e)
    print('{:>3} {:<6} {:<14} {:>6} {:>6} {:>6} {:>8} {:>8} {:>8}'.format(
        k, '第{}課'.format(k), lesson_titles[idx], ec, cc, nc,
        '{}-{}'.format(en_s,en_e), '{}-{}'.format(cn_s,cn_e), '{}-{}'.format(ne_s,ne_e)))
