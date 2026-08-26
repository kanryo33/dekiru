# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
pairs = json.load(open('med_zh_en_cn_map.json', encoding='utf-8'))
# 抽查：页4 (课2尾) 全部，以及几个关键词
print('=== 页4 全部 ===')
for pno, en, cn in pairs:
    if pno == 4:
        print(' EN:%s\n CN:%s' % (en, cn))
print('=== 含 グルメ/よさ/ポイント/エッセイ/驚き/おむつ 相关英文 ===')
for pno, en, cn in pairs:
    for kw in ['gourmet', 'goodness', 'point', 'essay', 'surprise', 'diaper', 'convenience', 'process', 'biomass', 'cocoa', 'overview', 'marri', 'day', 'soc', 'instit', 'monthly', 'easy']:
        if kw in en.lower():
            print('  p%d EN:%s => CN:%s' % (pno, en[:60], cn[:60]))
            break
