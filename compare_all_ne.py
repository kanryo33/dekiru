# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1) 本地 payload
payload = json.load(open('chuukyuu_payload.json', encoding='utf-8-sig'))
sheet = payload['sheets'][0]
cols = sheet['columns']
gi = cols.index('ネパール語') if 'ネパール語' in cols else cols.index('ne')
data = sheet['data']
# 确认列名
print('本地 payload 列:', cols)

# 2) 表格 G 列
gd = json.load(open('g_col2.json', encoding='utf-8-sig'))
ann = gd['data']['annotated_csv']
import re
sheet_rows = {}
for line in ann.split('\n'):
    line = line.strip()
    if line.startswith('[row='):
        m = re.match(r'\[row=(\d+)\] ?(.*)', line)
        if m:
            sheet_rows[int(m.group(1))] = m.group(2)

# 3) 逐行比对：payload 第 i 行 ↔ 表格第 i+2 行（表头占第1行）
diffs = []
for i, row in enumerate(data):
    row_no = i + 2
    local_ne = row[gi] if gi < len(row) else ''
    sheet_ne = sheet_rows.get(row_no, '')
    if local_ne != sheet_ne:
        diffs.append((row_no, local_ne, sheet_ne))

print(f'总词数: {len(data)}，比对完成')
print(f'不一致行数: {len(diffs)}')
for r, ln, sn in diffs[:30]:
    print(f'  row{r}: 本地={ln!r} | 表格={sn!r}')
