# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
pairs = json.load(open('med_zh_en_cn_map.json', encoding='utf-8'))
en = json.load(open('med_words_en.json', encoding='utf-8'))

def norm_en(s):
    s = s.lower()
    s = re.sub(r'[\u3040-\u30ff\u4e00-\u9fff\u3000-]', ' ', s)  # 去掉日文/中文字符
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# 官方映射：norm_en -> cn（去重，取最长英文的）
cn_map = {}
for pno, en0, cn in pairs:
    n = norm_en(en0)
    if not n:
        continue
    if n not in cn_map or len(en0) > cn_map[n][0]:
        cn_map[n] = (len(en0), en0, cn)
print('官方 cn_map 条数:', len(cn_map))

hits = 0
miss = []
for k in sorted(en, key=int):
    for (kanji, kana, etxt) in en[k]:
        n = norm_en(etxt)
        if n in cn_map:
            hits += 1
        else:
            miss.append((k, kanji, etxt, n))
print('第2版英文词条匹配官方中文: %d / %d' % (hits, hits + len(miss)))
print('未匹配 %d 条：' % len(miss))
for m in miss[:80]:
    print('  课%s %s | EN:%s | norm:%s' % (m[0], m[1], m[2][:50], m[3]))
