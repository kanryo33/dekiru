# -*- coding: utf-8 -*-
"""批量 image-ocr 处理中文 PDF 全部页 → 按栏/行提取 (日语,英语,中文) 存 JSON"""
import subprocess, json, sys, io, os, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ocr_page(png):
    r = subprocess.run(['mediakit-cli', 'image', 'image-ocr', '--image-url', os.path.abspath(png)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        return json.loads(r.stdout).get('ocr_result', [])
    except Exception:
        return []

def cluster_cols(blocks, x_split=600, gap=24):
    """按 x 分左右栏，各自按 y 聚类成行；返回 {L:[rows], R:[rows]}"""
    out = {'L': [], 'R': []}
    for side, flt in [('L', lambda x: x < x_split), ('R', lambda x: x >= x_split)]:
        items = sorted([(b['top_left_y'], b['top_left_x'], b['content']) for b in blocks if flt(b['top_left_x'])])
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

def split_row(tokens, side):
    """把行内 tokens 分为 日语/英语/中文 三段"""
    jp, en, zh = [], [], []
    for x, txt in tokens:
        if side == 'L':
            if x < 230: jp.append(txt)
            elif x < 395: en.append(txt)
            else: zh.append(txt)
        else:
            if x < 720: jp.append(txt)
            elif x < 875: en.append(txt)
            else: zh.append(txt)
    return ''.join(jp), ' '.join(en), ''.join(zh)

def norm_en(s):
    s = s.lower()
    s = re.sub(r'[^a-z\s]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def norm_zh(s):
    s = s.replace(' ', '')
    s = re.sub(r'[，、；：。！？…~～]', '', s)
    return s

def main():
    results = {}  # page -> [ {side, y, jp, en, zh} ]
    for png in sorted(glob.glob('zh_pages/zh_*.png')):
        page = os.path.basename(png)
        blocks = ocr_page(png)
        rows = cluster_cols(blocks)
        entries = []
        for side in ['L', 'R']:
            for r in rows[side]:
                jp, en, zh = split_row(r[1], side)
                if en or zh:
                    entries.append({'side': side, 'y': r[0], 'jp': jp, 'en': norm_en(en), 'zh': zh})
        results[page] = entries
        print(f'{page}: {len(entries)} 行')
        json.dump(results, open('med_zh_ocr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
