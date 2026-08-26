# -*- coding: utf-8 -*-
import subprocess, json, sys, io, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ocr_page(png):
    r = subprocess.run(['mediakit-cli', 'image', 'image-ocr', '--image-url', os.path.abspath(png)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return json.loads(r.stdout).get('ocr_result', [])

def cluster(blocks, x_split=600, gap=22):
    # 按 x 分左右栏，各自按 y 聚类成行；返回 {L: [行], R: [行]}
    out = {'L': [], 'R': []}
    for side, flt in [('L', lambda x: x < x_split), ('R', lambda x: x >= x_split)]:
        items = [(b['top_left_y'], b['top_left_x'], b['content']) for b in blocks if flt(b['top_left_x'])]
        items.sort(key=lambda t: (t[0], t[1]))
        rows = []
        cur = None
        for y, x, txt in items:
            if cur is None or y - cur[0] > gap:
                cur = [y, []]
                rows.append(cur)
            cur[1].append((x, txt))
        for r in rows:
            r[1].sort(key=lambda t: t[0])
        out[side] = rows
    return out

def classify_row(tokens):
    # 按 x 判断 日语/英语/中文：行内按 x 分三段
    # 日语 x<220px, 英语 220-480, 中文 >480 (左栏); 右栏日语>600...
    return tokens

if __name__ == '__main__':
    for png in ['zh_pages/zh_02.png']:
        blocks = ocr_page(png)
        rows = cluster(blocks)
        for side in ['L', 'R']:
            print(f'=== {side} ===')
            for r in rows[side]:
                parts = ' | '.join(txt for x, txt in r[1])
                print(f'y={r[0]:4d}  {parts[:90]}')
