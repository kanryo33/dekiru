# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open('med_zh_ocr.json', encoding='utf-8'))
for e in d['zh_01.png'][:40]:
    print('[' + e['side'] + ' y=' + str(e['y']) + '] jp=' + e['jp'][:16] + ' | en=' + e['en'][:30] + ' | zh=' + e['zh'][:24])
