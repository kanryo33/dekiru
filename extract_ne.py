# -*- coding: utf-8 -*-
import importlib.util, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
spec = importlib.util.spec_from_file_location('chuukyuu_words', 'chuukyuu_words.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
words = m.chuukyuu_words
out = []
for k in sorted(words.keys()):
    for idx, w in enumerate(words[k], 1):
        out.append(f'L{k}#{idx:>3} | {w["kanji"]} | {w["ne"]}')
open('ne_all.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(out))
