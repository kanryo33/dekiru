# -*- coding: utf-8 -*-
"""从中文PDF提取 (英文翻译 -> 中文翻译) 官方映射"""
import pymupdf, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
doc = pymupdf.open(r'E:\教科書\できる日本語＆漢字たまご\中級\語彙翻訳リスト\中国語.pdf')

def is_latin(s):
    return bool(re.search(r'[A-Za-z]', s)) and not re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', s)

def is_cjk(s):
    return bool(re.search(r'[\u4e00-\u9fff\u3001\u3002\uff08\uff09\u2014\u30fb]', s)) and not re.search(r'[A-Za-z]', s)

pairs = []  # (en, cn)
for pno in range(len(doc)):
    t = doc[pno].get_text()
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    en_buf = []
    pending = []  # [(idx, en_text)]
    page_pairs = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.isdigit() or '2014/03/27' in ln or 'できる日本語' in ln or ln in ('第','課'):
            i += 1; continue
        if is_latin(ln):
            # 收集连续英文行（一个翻译可能跨多行）
            en = ln
            j = i + 1
            while j < len(lines) and is_latin(lines[j]):
                en += ' ' + lines[j]
                j += 1
            page_pairs.append([en, None])
            i = j
        elif is_cjk(ln):
            # 中文行：赋给最近一个未填中文的英文
            if page_pairs and page_pairs[-1][1] is None:
                page_pairs[-1][1] = ln
            else:
                # 可能英文缺失，单独记录
                page_pairs.append([None, ln])
            i += 1
        else:
            i += 1
    for en, cn in page_pairs:
        if en and cn:
            pairs.append((en, cn))
    print('页%d: 提取 %d 对 (en,cn)' % (pno+1, len([p for p in page_pairs if p[0] and p[1]])), '共%d行' % len(lines))
    for p in page_pairs:
        if p[0] and not p[1]:
            print('  [en无cn]', p[0][:50])
        elif p[1] and not p[0]:
            print('  [cn无en]', p[1][:40])

json.dump(pairs, open('med_zh_en_cn_map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('总计 (en,cn) 对:', len(pairs))
