# -*- coding: utf-8 -*-
# 更新 index.html：加入中级20课（16-35）
import json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'D:\できる日本語 单词卡'
p = os.path.join(BASE, 'index.html')
s = open(p, encoding='utf-8').read()

TITLES = {
 1:'新しい出会い',2:'楽しい食事・上手な買い物',3:'時間を生かす',4:'地域を知って生活する',
 5:'緊急事態！',6:'地図を広げる',7:'世代を超えた交流',8:'気持ちを伝える',9:'言葉を楽しむ',
 10:'日本を旅する',11:'ライフスタイル',12:'心と体の健康',13:'トレンドに乗ってつながる',
 14:'カルチャーショック',15:'地域社会に生きる',16:'学校生活',17:'働くということ',
 18:'地球に生きる',19:'科学の力',20:'豊かさと幸せ'
}
app = json.load(open(os.path.join(BASE,'med_app_words.json'), encoding='utf-8'))

# ---- 1. 下拉菜单：初级包optgroup + 追加中级optgroup ----
m = re.search(r'<select id="lessonSelect">(.*?)</select>', s, re.S)
assert m, 'select not found'
old_options = m.group(1).strip()
new_select = ('<select id="lessonSelect">\n'
              '    <optgroup label="初級">\n'
              + old_options +
              '\n    </optgroup>\n'
              '    <optgroup label="中級">\n')
for i in range(1,21):
    new_select += '      <option value="%d">第%d課 %s</option>\n' % (15+i, i, TITLES[i])
new_select += '    </optgroup>\n  </select>'
s = s[:m.start()] + new_select + s[m.end():]

# ---- 2. 数据：在 lessonWordData 的收尾 }; 前插入 16-35 ----
m2 = re.search(r'const lessonWordData = \{(.*?)\n\};', s, re.S)
assert m2, 'lessonWordData not found'
block = m2.group(1)
for i in range(1,21):
    arr = app[str(i)]
    block += '\n  %d: %s,' % (15+i, json.dumps(arr, ensure_ascii=False))
s = s[:m2.start()] + 'const lessonWordData = {' + block + '\n};' + s[m2.end():]

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('index.html 已更新，中级20课(16-35)已加入')
