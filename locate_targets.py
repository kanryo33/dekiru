# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
lines = open('chuukyuu_words.py', encoding='utf-8').read().split('\n')
targets = ['イメージ','大きさ','ミステリー','遠慮','シール','ツイン','ポーチ','元気','さす','もう','水道','それに','気にする','ハート','おばさん','取り組む']
for i, l in enumerate(lines, 1):
    if any(t in l for t in targets):
        print(i, ':', l.strip()[:130])
