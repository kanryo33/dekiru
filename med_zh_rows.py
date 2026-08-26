# -*- coding: utf-8 -*-
import subprocess, json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ocr_page(png):
    r = subprocess.run(['mediakit-cli', 'image', 'image-ocr', '--image-url', os.path.abspath(png)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return json.loads(r.stdout).get('ocr_result', [])

def cluster_rows(blocks, gap=30):
    # blocks: {top_left_x, top_left_y, content, ...}
    items = []
    for b in blocks:
        items.append((b['top_left_y'], b['top_left_x'], b['content']))
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
    return rows

if __name__ == '__main__':
    png = 'zh_pages/zh_02.png'
    blocks = ocr_page(png)
    rows = cluster_rows(blocks)
    for r in rows:
        parts = ' | '.join(txt for x, txt in r[1])
        print(f'y={r[0]:4d}  {parts[:100]}')
