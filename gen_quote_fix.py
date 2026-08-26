# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 从比对结果提取 22 行不一致（表格值带首尾引号）
# 直接读本地 payload 的正确 ne 值
payload = json.load(open('chuukyuu_payload.json', encoding='utf-8-sig'))
sheet = payload['sheets'][0]
cols = sheet['columns']
gi = cols.index('ネパール語')
data = sheet['data']

gd = json.load(open('g_col.json', encoding='utf-8-sig'))
ann = gd['data']['annotated_csv']
import re
sheet_rows = {}
for line in ann.split('\n'):
    line = line.strip()
    if line.startswith('[row='):
        m = re.match(r'\[row=(\d+)\] ?(.*)', line)
        if m:
            sheet_rows[int(m.group(1))] = m.group(2)

writes = []
count = 0
for i, row in enumerate(data):
    row_no = i + 2
    local_ne = row[gi] if gi < len(row) else ''
    sheet_ne = sheet_rows.get(row_no, '')
    # 表格值 = 本地值 + 首尾各一个英文引号 → 需要清洗
    if sheet_ne == '"' + local_ne + '"':
        writes.append({
            "sheet_name": "全15課一覧",
            "range": f"G{row_no}",
            "cells": [[{"value": local_ne}]]
        })
        count += 1

with open('fix_quotes.json', 'w', encoding='utf-8') as f:
    json.dump(writes, f, ensure_ascii=False)
print(f'待清洗引号行数: {count}')
