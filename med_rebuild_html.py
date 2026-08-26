# -*- coding: utf-8 -*-
# 重构 index.html：三级（初級/初中級/中級）等级下拉 + 课程下拉联动
import json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'/Users/kanryo/Documents/工作空间/できる日本語_单词卡_项目'
p = os.path.join(BASE, 'index.html')
s = open(p, encoding='utf-8').read()

# ---------- 1. 收集三个等级的数据 ----------
# 初级：app_words.json {1..15: [...]}
primary = json.load(open(os.path.join(BASE,'app_words.json'), encoding='utf-8'))
# 中级：med_app_words.json {1..20: [...]}
interm  = json.load(open(os.path.join(BASE,'med_app_words.json'), encoding='utf-8'))
# 初中级：chuukyuu_payload.json sheets[0].data
ch = json.load(open(os.path.join(BASE,'chuukyuu_payload.json'), encoding='utf-8'))
ch_rows = ch['sheets'][0]['data']
chuukyuu = {}
for r in ch_rows:
    lesson_no = int(re.match(r'第(\d+)課', r[0]).group(1))
    entry = {'kanji': r[2], 'kana': r[3], 'eng': r[4], 'cn': r[5], 'ne': r[6]}
    chuukyuu.setdefault(lesson_no, []).append(entry)
print('初中级课数:', len(chuukyuu), '总词数:', sum(len(v) for v in chuukyuu.values()))

# ---------- 2. 课标题 ----------
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
    return '{' + ','.join('%d:"%s"'%(k,v) for k,v in titles.items()) + '}'

def js_data(data):
    return '{' + ','.join('%d:%s'%(int(k), json.dumps(v, ensure_ascii=False)) for k,v in data.items()) + '}'

LEVEL_DATA_JS = ('const LEVEL_DATA = {\n'
  '  "初級": { lessons: %s, data: %s },\n'
  '  "初中級": { lessons: %s, data: %s },\n'
  '  "中級": { lessons: %s, data: %s }\n'
  '};' % (js_lessons(PRIMARY_TITLES), js_data(primary),
          js_lessons(CHUUKYUU_TITLES), js_data(chuukyuu),
          js_lessons(INTERM_TITLES), js_data(interm)))

# ---------- 3. 替换 HTML：下拉 ----------
old_select = r'<select id="lessonSelect">.*?</select>'
new_select = ('<div class="level-bar">\n'
 '    <select id="levelSelect">\n'
 '      <option value="初級">初級</option>\n'
 '      <option value="初中級">初中級</option>\n'
 '      <option value="中級">中級</option>\n'
 '    </select>\n'
 '    <select id="lessonSelect"></select>\n'
 '  </div>')
s2, n1 = re.subn(old_select, new_select, s, count=1, flags=re.S)
assert n1==1, 'select replace failed'
s = s2

# ---------- 4. 替换脚本 ----------
# 4.1 数据块
m = re.search(r'const lessonWordData = \{.*?\n\};', s, re.S)
assert m, 'lessonWordData not found'
s = s[:m.start()] + LEVEL_DATA_JS + s[m.end():]

# 4.2 初始化变量
old_init = 'let currentLesson = 1;\nlet wordData = [...lessonWordData[currentLesson]];'
new_init = ('let currentLevel = "初級";\n'
 'let currentLesson = 1;\n'
 'let wordData = [...LEVEL_DATA[currentLevel].data[currentLesson]];')
assert old_init in s, 'init not found'
s = s.replace(old_init, new_init)

# 4.3 changeLesson 函数
old_cl = ('function changeLesson(n){\n'
 '  currentLesson = n;\n'
 '  wordData = [...lessonWordData[n]];\n'
 '  safeSwitchIndex(0);\n'
 '}')
new_cl = ('function rebuildLessonOptions(level){\n'
 '  lessonSelect.innerHTML = "";\n'
 '  const L = LEVEL_DATA[level];\n'
 '  Object.keys(L.lessons).sort((a,b)=>a-b).forEach(k=>{\n'
 '    const o = document.createElement("option");\n'
 '    o.value = k;\n'
 '    o.textContent = "第" + k + "課 " + L.lessons[k];\n'
 '    lessonSelect.appendChild(o);\n'
 '  });\n'
 '}\n'
 'function changeLevel(){\n'
 '  currentLevel = levelSelect.value;\n'
 '  rebuildLessonOptions(currentLevel);\n'
 '  changeLesson(+lessonSelect.value);\n'
 '}\n'
 'function changeLesson(n){\n'
 '  currentLesson = n;\n'
 '  wordData = [...LEVEL_DATA[currentLevel].data[n]];\n'
 '  safeSwitchIndex(0);\n'
 '}')
assert old_cl in s, 'changeLesson not found'
s = s.replace(old_cl, new_cl)

# 4.4 lessonSelect listener 前插入 levelSelect 处理 + 初始化
old_lis = 'lessonSelect.addEventListener("change", e => changeLesson(+e.target.value));'
new_lis = ('const levelSelect = document.getElementById("levelSelect");\n'
 'levelSelect.addEventListener("change", changeLevel);\n'
 'lessonSelect.addEventListener("change", e => changeLesson(+e.target.value));\n'
 'rebuildLessonOptions(currentLevel);')
assert old_lis in s, 'listener not found'
s = s.replace(old_lis, new_lis)

# ---------- 5. CSS：level-bar 样式 ----------
old_css = '.mode-bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center;}'
new_css = ('.level-bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center;}\n'
 '.mode-bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center;}')
if old_css in s:
    s = s.replace(old_css, new_css, 1)

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('index.html 重构完成')
