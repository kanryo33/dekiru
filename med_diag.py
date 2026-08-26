# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
pairs = json.load(open('med_zh_en_cn_map.json', encoding='utf-8'))
zh = json.load(open('med_zh_read.json', encoding='utf-8'))
en = json.load(open('med_words_en.json', encoding='utf-8'))

def norm_en(s):
    s = s.lower()
    s = re.sub(r'[\u3040-\u30ff\u4e00-\u9fff\u3000-]', ' ', s)
    s = re.sub(r"[’']", ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# 1. map 里有没有这些英文
test_en = ['quality', 'tent', 'actor', 'politics', 'agriculture', 'theory', 'diplomacy',
           'government', 'cell', 'unit', 'income', 'rights', 'image', 'edit', 'send',
           'multiple', 'trend', 'exam', 'previous year', 'basic', 'birth', 'couple',
           'aware', 'add', 'life', 'kitchen', 'kitchen equipment', 'pot', 'distance',
           'radio', 'report', 'broadcast', 'distance']
for t in test_en:
    found = [ (p, e, c) for p, e, c in pairs if t in norm_en(e)]
    print('== %s == map命中:%d' % (t, len(found)))
    for f in found[:3]:
        print('    p%d EN:%s CN:%s' % (f[0], f[1][:40], f[2][:30]))

# 2. zh_read 里有没有这些日文词条
test_jp = ['品質', '協会', '俳優', '政治', '農業', '理論', '外交', '政府', '細胞', '単位', '収入', '権利', '画像', '編集', '送信', '複数', '傾向', '前年', '基本', '出生', '夫婦', '自覚', '加える', 'ため', 'テント']
for t in test_jp:
    hits = []
    for page, entries in zh.items():
        for jp, cn in entries:
            if t in jp:
                hits.append((page, jp, cn))
    print('== %s == zh_read:%d' % (t, len(hits)), hits[:3])
