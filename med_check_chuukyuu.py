# -*- coding: utf-8 -*-
import sys, io, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
spec = importlib.util.spec_from_file_location('cw', 'chuukyuu_words.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
w = m.chuukyuu_words
print('初中级第1课词序（前30）:')
for i, item in enumerate(w[1][:30], 1):
    print(f'  {i}. {item["kanji"]} ({item["kana"]})')
