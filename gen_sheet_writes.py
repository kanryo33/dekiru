# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# (row, 新 ne) —— row 基于飞书表格实际行号（表头第1行，数据从第2行起）
fixes = [
    (61,  'कल्पना गर्नु'),
    (96,  'अर्को ～ (जस्तै: अर्को एक कप)'),
    (197, 'काकी'),
    (204, 'पानीको धारा'),
    (268, 'आकार'),
    (274, 'मुटुको आकार'),
    (378, 'अनि त्यसका साथै'),
    (413, 'रहस्य / मिस्ट्री'),
    (468, 'नम्रतापूर्वक अस्वीकार गर्नु'),
    (541, 'स्टिकर'),
    (620, 'ट्विन'),
    (627, 'पाउच / थैली'),
    (766, 'सञ्चो'),
    (774, 'छाता लगाउनु / उघार्नु'),
    (814, 'ध्यान गर्नु'),
    (968, 'मिहिनेत गर्नु'),
]

writes = []
for row, ne in fixes:
    writes.append({
        "sheet_name": "全15課一覧",
        "range": f"G{row}",
        "cells": [[{"value": ne}]]
    })

with open('fix_sheet_writes.json', 'w', encoding='utf-8') as f:
    json.dump(writes, f, ensure_ascii=False)
print(f'已生成 {len(writes)} 条写入，写入文件 fix_sheet_writes.json')
