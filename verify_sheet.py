# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.load(open('g_col.json', encoding='utf-8-sig'))
ann = data['data']['annotated_csv']
rows = {}
for line in ann.split('\n'):
    line = line.strip()
    if line.startswith('[row='):
        m = re.match(r'\[row=(\d+)\] ?(.*)', line)
        if m:
            rows[int(m.group(1))] = m.group(2)
targets = [61,96,197,204,268,274,378,413,468,541,620,627,766,774,814,968]
for t in targets:
    print(f'row{t}: {rows.get(t, "(缺失)")}')
