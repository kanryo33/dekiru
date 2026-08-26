# -*- coding: utf-8 -*-
"""从 chuukyuu_words.py 生成飞书表格建表 payload JSON"""
import json, importlib.util, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

spec = importlib.util.spec_from_file_location('chuukyuu_words', 'chuukyuu_words.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
words = m.chuukyuu_words

lesson_names = {
    1:'新しい一歩', 2:'楽しいショッピング', 3:'私の目標', 4:'住んでいる町で',
    5:'大変な1日', 6:'旅行に行こう', 7:'西川さんの家へ', 8:'ありがとう',
    9:'アルバイト先で', 10:'旅行に行って', 11:'地域社会の中で', 12:'私の健康法',
    13:'親の気持ち・子の気持ち', 14:'イベント・行事', 15:'気になるニュース'
}

data = []
problems = []
total = 0
special_kana = {'マッサージ器':'マッサージき'}  # 混写词的注音例外
for k in sorted(words.keys()):
    lst = words[k]
    for idx, w in enumerate(lst, start=1):
        total += 1
        kanji = w['kanji']; kana = w.get('kana','').strip()
        if not kana:
            kana = special_kana.get(kanji, kanji)  # 片假名词/假名自身 → 注音=自身
        for f in ('kanji','kana','eng','cn','ne'):
            if not str(w.get(f,'')).strip():
                problems.append(f'L{k}#{idx} 缺字段 {f}: {w}')
        data.append([f'第{k}課', idx, kanji, kana, w['eng'], w['cn'], w['ne']])

print(f'总词数: {total}')
print(f'缺失字段数: {len(problems)}')
for p in problems[:20]:
    print('  ', p)

payload = {
    "sheets": [
        {
            "name": "全15課一覧",
            "columns": ["課","番号","単語","よみ","英語","中国語","ネパール語"],
            "data": data,
            "dtypes": {"課":"object","番号":"object","単語":"object","よみ":"object","英語":"object","中国語":"object","ネパール語":"object"}
        }
    ]
}

with open('chuukyuu_payload.json','w',encoding='utf-8',newline='\n') as f:
    json.dump(payload, f, ensure_ascii=False)
print('payload 已写入 chuukyuu_payload.json')
