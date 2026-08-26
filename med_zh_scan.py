# -*- coding: utf-8 -*-
import subprocess, json, sys, io, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 用 image-ocr 扫描每页，输出文本块摘要定位词汇页
results = {}
for png in sorted(glob.glob('zh_pages/zh_*.png')):
    page = os.path.basename(png)
    r = subprocess.run(['mediakit-cli', 'image', 'image-ocr', '--image-url', os.path.abspath(png)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        data = json.loads(r.stdout)
        blocks = data.get('ocr_result', [])
        # 汇总该页所有文本
        texts = [b.get('content', '') for b in blocks]
        joined = ' '.join(texts)
        # 检测课标题
        import re
        lessons = re.findall(r'\d+\s*课', joined)
        has_english = any('to ' in t or 'the ' in t for t in texts)
        results[page] = {'n': len(blocks), 'has_lesson': lessons[:8], 'has_eng': has_english,
                         'sample': ' '.join(texts[:6])[:120]}
    except Exception as e:
        results[page] = {'error': str(e)}

for p in sorted(results):
    r = results[p]
    print(p + ': n=' + str(r.get('n')) + ' lesson=' + str(r.get('has_lesson')) + ' eng=' + str(r.get('has_eng')) + ' | ' + str(r.get('sample', '')))
