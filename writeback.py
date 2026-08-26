# -*- coding: utf-8 -*-
import json, os, shutil

src = 'med_trilingual_clean2.json'
dst = 'med_trilingual.json'

d = json.load(open(src, encoding='utf-8'))
# 保险：确保 bak 存在
if not os.path.exists(dst + '.bak'):
    shutil.copy(dst, dst + '.bak')
json.dump(d, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('写回完成:', dst, '共', len(d), '条')

# 对比差异条数（与 bak）
bak = json.load(open(dst + '.bak', encoding='utf-8'))
diff = 0
bm = {(r['lesson'], r['no']): r['ne'] for r in bak}
for r in d:
    if bm.get((r['lesson'], r['no'])) != r['ne']:
        diff += 1
print('与原始数据相比，ne 字段变更条数:', diff)
