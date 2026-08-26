《できる日本語》三语单词卡 项目说明
====================================

■ 项目内容
本文件夹是《できる日本語》系列教材（初級 / 初中級 / 中級）的
「日・英・中・尼泊尔语」四语单词卡项目，供课堂上投影使用。

■ 单词卡程序（核心交付）
  index.html
  - 打开即可使用（浏览器直接打开，无需服务器）
  - 两个下拉菜单：先选「等级」（初級/初中級/中級），再选「课程」
  - 单词卡片正面/背面翻转显示，支持两种模式：
      ① 漢字→読み・意味
      ② 英・中・ネパール語→日本語
  - 大字大卡，适合投影（透视已调平，翻转无位移）

■ 三个等级数据文件
  初級   app_words.json                （15课, 744词）
  初中級 chuukyuu_payload.json         （15课, 1030词）
  中級   med_trilingual.json           （20课, 2288词，含 lesson/no/kanji/kana/en/cn/ne/src）
  中級   med_app_words.json            （中級，可直接并入单词卡的数据）
  中級   med_trilingual_sheet.json     （中級，飞书表格用结构）

■ 词汇表（Excel）
  中级词汇表.xlsx                      （中級20课三语完整表）
  单词卡词汇完整性校验报告.xlsx        （初級补全校验报告）

■ 说明
  - 中級尼语有38词在官方尼语PDF中不存在，表格/卡片中标注为
    「（公式リストになし）」
  - 中級以第2版英文词表为骨架，中文翻译来自官方PDF+OCR+手工补译

■ 脚本（供继续开发/重新生成用）
  med_final4.py        中級三语合并构建（改 med_miss_override.py 补译后重跑）
  med_fix_ne.py        尼语匹配改进与缺失清单
  med_miss_override.py 手工补译表（OVERRIDE 字典）
  med_gen_delivery.py  生成 Excel / sheets JSON / 单词卡数据
  med_rebuild_html.py  重构单词卡 index.html（三级下拉联动）
  med_extract_cn2.py   中文PDF坐标法提取(en→cn)映射
  其他 med_*.py        提取/OCR/核对辅助脚本

■ 目录
  zh_pages/  ne_pages/    PDF逐页渲染图（OCR中间产物，可删）
  其他 .py/.txt/.json     处理过程中的中间产物

■ 在别的电脑继续使用
  1. 双击 index.html 即可用单词卡
  2. 需改词汇/重新生成时，确保电脑装有 Python3 + pymupdf + openpyxl，
     修改脚本后执行：python -X utf8 脚本名.py
  3. 源PDF（官方三语词汇PDF）不在本文件夹内，在教科书目录，如要继续提取需带上
