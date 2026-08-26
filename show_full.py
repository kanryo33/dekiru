# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
lines = open('chuukyuu_words.py', encoding='utf-8').read().split('\n')
for n in [102, 207, 484, 657, 792, 800, 840, 1000, 286, 649, 392]:
    print(n, ':', lines[n-1])
