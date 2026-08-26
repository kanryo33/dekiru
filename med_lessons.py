# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
lines = open('med_英語_lines.txt', encoding='utf-8').read().split('\n')

# 1) 找所有"第 N課"标题行（含假名注音行）
print('=== 第N課 标题位置 ===')
for i, l in enumerate(lines, 1):
    m = re.search(r'第\s*(\d+)\s*課', l)
    if m and '====' not in l:
        print(f'{i}: {l.strip()}')
