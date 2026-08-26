# -*- coding: utf-8 -*-
# 更新 index.html 中 LEVEL_DATA 数据块（用修正后的 med_app_words.json）
import json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'/Users/kanryo/Documents/工作空间/できる日本語_单词卡_项目'
p = os.path.join(BASE, 'index.html')
s = open(p, encoding='utf-8').read()

primary = json.load(open(os.path.join(BASE, 'app_words.json'), encoding='utf-8'))
interm  = json.load(open(os.path.join(BASE, 'med_app_words.json'), encoding='utf-8'))
ch = json.load(open(os.path.join(BASE, 'chuukyuu_payload.json'), encoding='utf-8'))
ch_rows = ch['sheets'][0]['data']
chuukyuu = {}
for r in ch_rows:
    lesson_no = int(re.match(r'第(\d+)課', r[0]).group(1))
    entry = {'kanji': r[2], 'kana': r[3], 'eng': r[4], 'cn': r[5], 'ne': r[6]}
    chuukyuu.setdefault(lesson_no, []).append(entry)

PRIMARY_TITLES = {
 1:'はじめまして',2:'買い物・食事',3:'スケジュール',4:'私の国・町',5:'休みの日',
 6:'一緒に!',7:'友達の家で',8:'大切な人',9:'好きなこと',10:'バスツアー',
 11:'私の生活',12:'病気・けが',13:'私のおすすめ',14:'国・町の習慣',15:'イベント情報・ニュースから'}
CHUUKYUU_TITLES = {
 1:'新しい一歩',2:'楽しいショッピング',3:'私の目標',4:'住んでいる町で',5:'大変な1日',
 6:'旅行に行こう',7:'西川さんの家へ',8:'ありがとう',9:'アルバイト先で',10:'旅行に行って',
 11:'地域社会の中で',12:'私の健康法',13:'親の気持ち・子の気持ち',14:'イベント・行事',15:'気になるニュース'}
INTERM_TITLES = {
 1:'新しい出会い',2:'楽しい食事・上手な買い物',3:'時間を生かす',4:'地域を知って生活する',
 5:'緊急事態！',6:'地図を広げる',7:'世代を超えた交流',8:'気持ちを伝える',9:'言葉を楽しむ',
 10:'日本を旅する',11:'ライフスタイル',12:'心と体の健康',13:'トレンドに乗ってつながる',
 14:'カルチャーショック',15:'地域社会に生きる',16:'学校生活',17:'働くということ',
 18:'地球に生きる',19:'科学の力',20:'豊かさと幸せ'}

def js_lessons(titles):
    return '{' + ','.join('%d:"%s"' % (k, v) for k, v in titles.items()) + '}'

def js_data(data):
    return '{' + ','.join('%d:%s' % (int(k), json.dumps(v, ensure_ascii=False)) for k, v in data.items()) + '}'

LEVEL_DATA_JS = ('const LEVEL_DATA = {\n'
  '  "初級": { lessons: %s, data: %s },\n'
  '  "初中級": { lessons: %s, data: %s },\n'
  '  "中級": { lessons: %s, data: %s }\n'
  '};' % (js_lessons(PRIMARY_TITLES), js_data(primary),
          js_lessons(CHUUKYUU_TITLES), js_data(chuukyuu),
          js_lessons(INTERM_TITLES), js_data(interm)))

m = re.search(r'const LEVEL_DATA = \{(.*?)\n\};', s, re.S)
assert m, 'LEVEL_DATA block not found'
s = s[:m.start()] + LEVEL_DATA_JS + s[m.end():]

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('LEVEL_DATA 数据块已更新')
# 验证中級数据条数
print('中級总词数:', sum(len(v) for v in interm.values()))
