# -*- coding: utf-8 -*-
"""中级三语词汇表 v5：
CN优先级: official(en精确) > zhocr(kanji) > ensub(en去括号) > entok(en token) > sub(kanji前缀) > added(补译)
"""
import json, sys, io, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en = json.load(open('med_words_en.json', encoding='utf-8'))
ne = json.load(open('med_words_ne.json', encoding='utf-8'))
zh = json.load(open('med_zh_read.json', encoding='utf-8'))
pairs = json.load(open('med_zh_en_cn_map.json', encoding='utf-8'))

def norm(s):
    if not s: return ''
    s = s.replace(' ', '').replace('\u3000', '').replace('〜', '～')
    for a, b in zip('０１２３４５６７８９', '0123456789'):
        s = s.replace(a, b)
    return s
def strip_bracket(s):
    return re.sub(r'[（(].*?[）)]', '', s)
def main_part(s):
    return re.split(r'[（(]', s)[0].strip()
def norm_en(s):
    s = s.lower()
    s = re.sub(r'[\u3040-\u30ff\u4e00-\u9fff\u3000-]', ' ', s)
    s = re.sub(r"[’']", ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# 官方 map
cn_map = {}
for pno, en0, cn in pairs:
    n = norm_en(en0)
    if not n: continue
    if n not in cn_map:
        cn_map[n] = (len(en0), cn)
# 去括号版 map（en 去掉 [here...] 等）
cn_map2 = {}
for n, (L, cn) in cn_map.items():
    pass

def find_official(en_txt):
    n = norm_en(en_txt)
    if n and n in cn_map:
        return cn_map[n][1], 'official'
    # 去括号注释再匹配
    n2 = re.sub(r'\[[^\]]*\]', '', en_txt)
    n2 = re.sub(r'\([^)]*\)', '', n2)
    n2 = norm_en(n2)
    if n2 and n2 in cn_map:
        return cn_map[n2][1], 'official'
    return None, None

def find_ensub(en_txt):
    # token 匹配：en_txt 的核心 token 与 map key 有 >=2 个相同 token
    toks = set(norm_en(en_txt).split())
    if len(toks) < 3: return None
    # 去除停用词后的核心词
    stop = {'to','the','a','an','of','and','in','on','for','with','at','by','from','up','down','out','off','into','as','is','are','be','it','its','that','this','one','you','here','there','they','their','or','so','very','much','more','most','not','no','do','does','can','will','would','should','all','any','some','etc','per'}
    core = toks - stop
    if len(core) < 2: return None
    best = None
    for n, (L, cn) in cn_map.items():
        nset = set(n.split())
        inter = core & nset
        if len(inter) >= 2 and (len(nset) <= len(core) + 2):
            score = len(inter) + 0.5 * min(len(nset), len(core)) / max(len(nset), len(core))
            if best is None or score > best[0]:
                best = (score, cn)
    return best[1] if best else None

# zh_read
zh_map = {}
zh_mainmap = {}
zh_full = []
for page, entries in zh.items():
    for (jp, cn) in entries:
        zh_full.append((jp, cn))
        for k in {norm(jp), norm(strip_bracket(jp)), norm(main_part(jp)), norm(jp.replace('-', ''))}:
            if k:
                zh_map.setdefault(k, (jp, cn))
        mp = norm(main_part(jp))
        if mp:
            zh_mainmap.setdefault(mp, []).append((jp, cn))
def find_zh(kanji, kana):
    for key in [norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', '')), norm(kana)]:
        if key and key in zh_map:
            return zh_map[key], 'zhocr'
    # sub 前缀
    c3 = norm(main_part(kanji))
    if c3 and len(c3) >= 2:
        for jp, cno in zh_full:
            zmp = norm(main_part(jp))
            if zmp and len(zmp) >= 2 and (zmp.startswith(c3) or c3.startswith(zmp)) and len(zmp) - len(c3) <= 3:
                return (jp, cno), 'sub'
    return None, None

# NE
ne_map = {}
for k, items in ne.items():
    for (kanji, kana, netxt) in items:
        for kk in {norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))}:
            if kk:
                ne_map.setdefault(kk, netxt)
def find_ne(kanji):
    for kk in [norm(kanji), norm(strip_bracket(kanji)), norm(main_part(kanji)), norm(kanji.replace('-', ''))]:
        if kk and kk in ne_map:
            return ne_map[kk]
    return ''

def fix_kanji(kanji):
    k = re.sub(r'\[.*?\]', '', kanji)
    if k.count('（') > k.count('）'): k += '）'
    if k.count('(') > k.count(')'): k += ')'
    return k

# ---- override 补译（第2版新增/旧版用词不同）----
override = {
 'よさ':'好处，优点','グルメ':'美食','簡易':'简易','なぜか':'不知为何','名産':'名产',
 '最大':'最大','中古':'二手','学園':'学园','早口':'语速快','ほっぺたが落ちる':'好吃得不得了',
 'いざ':'关键时刻；一旦','～機関（国際機関':'～机构（国际机构）','気楽さ':'轻松自在',
 '社会保障':'社会保障','おむつ':'尿布','日数':'天数','未婚':'未婚','ポイント':'要点，重点',
 '印象的（な）':'令人印象深刻的','熱気':'热情','エッセイ':'随笔，散文',
 'もの（ものの考え方':'事物（事物的想法）','向き合う':'面对面，正视','プラスチック':'塑料',
 '驚き':'惊讶','永久':'永久','可能性':'可能性','便利さ':'便利性','上り下り-する':'上下（山）',
 '何の～もない（何の関係もない':'毫无～（毫无关系）','国語[教科名':'国语','野生':'野生',
 'ファンクラブ':'粉丝俱乐部','思い通り':'如自己所愿','電源構成':'电源构成','地熱':'地热',
 '過程':'过程','バイオマス':'生物质','バブル景気':'泡沫经济','数値':'数值','カカオ豆':'可可豆',
 '概要':'概要',
}

# ---- 课19/20 第2版新增词补译（旧版中文无对应）----
override2 = {
 # 课19
 '認識-する':'认识，认知','生命':'生命','幼稚園':'幼儿园','進歩-する':'进步','手を抜く':'偷工减料',
 '指す':'指，指向','生み出す':'创造出，产生','生む':'产生，生出','徒歩':'步行','ありがたさ':'可贵之处',
 '手をかける':'花心思，精心照料','変異-する':'变异','遺伝-する':'遗传','巻頭言':'卷首语','協同-する':'协同',
 '先端':'尖端，前沿','浮く':'浮起','洗い物':'要洗的东西','引く（関心を引く）':'吸引（引起关注）',
 '兆':'兆（万亿）','天然ガス':'天然气','体外':'体外','拒絶-する':'排斥，拒绝','自身':'自身，本身',
 '体中':'全身','実用':'实用','優れる':'优秀，出色','物語':'故事','建築-する':'建筑','理論':'理论',
 '外交':'外交','相容れない':'互不相容','農業':'农业','根本':'根本','ゲノム編集':'基因组编辑',
 '栄養価':'营养价值','品種':'品种','悪者':'坏人','あくまでも':'说到底，归根结底','作物':'农作物',
 '喜び':'喜悦，高兴','良しとする':'认可，视为妥当','間（長い間':'期间（长年累月）','政治':'政治',
 '前者':'前者','振る':'挥，摇','あまりに':'过于','万が一':'万一','癒し':'治愈','かわいがる':'疼爱',
 '触れ合う':'接触，交流','戦後':'战后','脱～（脱原発':'脱离～（去核电）','原発':'核电站',
 '再生可能エネルギー':'可再生能源','主要（な）':'主要的','需要':'需求','ますます':'越来越',
 '考慮-する':'考虑','組み合わせる':'组合，搭配','断念-する':'放弃','細胞':'细胞','再生医療':'再生医疗',
 # 课20
 '第～（第20課':'第～（第20课）','志向-する':'志向，致力于','冒険-する':'冒险','発熱-する':'发烧',
 '嘔吐-する':'呕吐','発症-する':'发病','重症化-する':'重症化','競争-する':'竞争','低下-する':'下降',
 '学士':'学士','迷い':'迷茫，犹豫','出合い':'相遇','決心-する':'下决心','省く':'省去，省略',
 '衝撃':'冲击','重さ':'重量','単位':'学分，单位','収入':'收入','マラリア':'疟疾','交渉-する':'谈判',
 '権利':'权利','クラウドファンディング':'众筹','加工-する':'加工','境界線':'分界线','溶かす':'溶化，溶解',
 'キャッチフレーズ':'宣传口号','経る':'经过，经历','政府':'政府','［国内総生産':'（国内生产总值）',
 '質的（な）':'质的','質':'质量，本质','我が～（我が国':'我～（我国）','ウェルビーイング（Well-':'福祉（幸福感）',
 '怖さ':'可怕','冒険':'冒险','単位（単位':'（单位）','発症':'发病',
}

rows = []
src_cnt = Counter()
problems = []
for k in sorted(en, key=int):
    for idx, (kanji, kana, etxt) in enumerate(en[k], 1):
        cn = src = None
        # 1 official
        cn, src = find_official(etxt)
        if not cn:
            # 2 zhocr
            hit, src2 = find_zh(kanji, kana)
            if hit:
                cn, src = hit[1], src2
        if not cn:
            # 3 ensub
            cn = find_ensub(etxt)
            if cn:
                src = 'ensub'
        if not cn:
            # 4 override
            mp = main_part(kanji).strip()
            if mp in override:
                cn, src = override[mp], 'added'
            elif kanji in override:
                cn, src = override[kanji], 'added'
            elif mp in override2:
                cn, src = override2[mp], 'added'
            elif kanji in override2:
                cn, src = override2[kanji], 'added'
        if not cn:
            src = 'miss'
            problems.append((k, kanji, etxt))
        src_cnt[src] += 1
        rows.append({
            'lesson': int(k), 'no': idx, 'kanji': fix_kanji(kanji), 'kana': kana,
            'en': etxt, 'cn': cn if cn else '', 'ne': find_ne(kanji), 'src': src
        })

print('来源统计:', dict(src_cnt))
print('仍缺中文:', len(problems))
for p in problems:
    print(' ', p)
json.dump(rows, open('med_trilingual.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入 med_trilingual.json, 总词条:', len(rows))
