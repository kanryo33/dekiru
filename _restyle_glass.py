# -*- coding: utf-8 -*-
# 用「液态玻璃 Liquid Glass」风格重写 index.html 的 head/style/body 标记层。
# 脚本部分（数据 + 逻辑）原样保留，只在 </body> 前追加一个指针高光增强脚本。
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
BASE = r'/Users/kanryo/Documents/工作空间/できる日本語_单词卡_项目'
p = os.path.join(BASE, 'index.html')
s = open(p, encoding='utf-8').read()

MARKUP = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#e8ecf7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f1e" media="(prefers-color-scheme: dark)">
<title>日本語単語カード Pro</title>
<style>
/* ============ 液态玻璃 Liquid Glass 设计系统 ============ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
*{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display","Hiragino Sans","Noto Sans JP","Yu Gothic UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;}

:root{
  color-scheme:light dark;
  --ink:#1c2244;
  --ink-soft:#49517a;
  --muted:#68719a;
  --page:#e8ecf7;
  --glass-hi:rgba(255,255,255,.66);
  --glass-lo:rgba(255,255,255,.36);
  --glass-grad:linear-gradient(165deg,var(--glass-hi),var(--glass-lo));
  --glass-border:rgba(255,255,255,.62);
  --rim:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(255,255,255,.3);
  --drop:0 26px 56px -20px rgba(23,34,80,.28),0 4px 14px rgba(23,34,80,.08);
  --track:rgba(255,255,255,.45);
  --track-border:rgba(255,255,255,.42);
  --top-light:rgba(255,255,255,.5);
  --seg-track:rgba(94,108,160,.16);
  --seg-border:rgba(255,255,255,.45);
  --seg-ink:#4a5378;
  --kbd-bg:rgba(255,255,255,.6);
  --kbd-border:rgba(255,255,255,.8);
  --kbd-ink:#3a4368;
  --focus:0 0 0 4px rgba(99,110,255,.28);
  --en-ink:#2f57d6;
  --ne-ink:#7a3fd4;
  --cn-ink:#47506e;
  --grain:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E");
  --chev:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1.5l5 5 5-5' fill='none' stroke='%235b6478' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}
@media (prefers-color-scheme: dark){
  :root{
    --ink:#eef1ff;
    --ink-soft:#c9d1ee;
    --muted:#98a2c8;
    --page:#0b0f1e;
    --glass-hi:rgba(70,78,120,.55);
    --glass-lo:rgba(30,35,60,.38);
    --glass-border:rgba(255,255,255,.16);
    --rim:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -1px 0 rgba(255,255,255,.05);
    --drop:0 26px 56px -18px rgba(0,0,0,.6),0 4px 14px rgba(0,0,0,.3);
    --track:rgba(255,255,255,.14);
    --track-border:rgba(255,255,255,.14);
    --top-light:rgba(255,255,255,.1);
    --seg-track:rgba(8,12,28,.4);
    --seg-border:rgba(255,255,255,.12);
    --seg-ink:#b6bfe4;
    --kbd-bg:rgba(255,255,255,.12);
    --kbd-border:rgba(255,255,255,.18);
    --kbd-ink:#c9d1ee;
    --en-ink:#8fb0ff;
    --ne-ink:#c39bff;
    --cn-ink:#c4cbe6;
    --chev:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1.5l5 5 5-5' fill='none' stroke='%23cdd5ee' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  }
}

/* ---------- 背景：流动的极光色场（玻璃的“液体”来源） ---------- */
body{
  min-height:100vh;display:flex;flex-direction:column;align-items:center;gap:22px;padding:26px 16px 36px;
  background:var(--page);position:relative;overflow-x:hidden;
}
.bg{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none;}
.orb{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55;will-change:transform;}
.o1{width:44vmax;height:44vmax;background:#7fb2ff;top:-18vmax;left:-12vmax;animation:drift1 26s ease-in-out infinite alternate;}
.o2{width:38vmax;height:38vmax;background:#d0a2ff;bottom:-16vmax;right:-10vmax;animation:drift2 32s ease-in-out infinite alternate;}
.o3{width:26vmax;height:26vmax;background:#ffc4e3;top:30%;right:-8vmax;animation:drift3 29s ease-in-out infinite alternate;}
.o4{width:24vmax;height:24vmax;background:#9df0d4;bottom:6%;left:-8vmax;animation:drift1 35s ease-in-out infinite alternate-reverse;}
.o5{width:20vmax;height:20vmax;background:#ffe1b0;top:-6vmax;right:24vw;animation:drift2 38s ease-in-out infinite alternate-reverse;}
@keyframes drift1{to{transform:translate(9vmax,7vmax) scale(1.08);}}
@keyframes drift2{to{transform:translate(-8vmax,-6vmax) scale(1.1);}}
@keyframes drift3{to{transform:translate(-6vmax,8vmax) scale(.92);}}
.bg::after{content:'';position:absolute;inset:0;background-image:var(--grain);opacity:.05;}
@media (prefers-color-scheme: dark){ .orb{opacity:.30;} .bg::after{opacity:.07;} }

/* ---------- 顶部玻璃控制台 ---------- */
.top-bar{
  position:relative;width:100%;max-width:1200px;z-index:10;
  display:flex;flex-direction:column;align-items:center;gap:14px;
  padding:18px 22px 20px;border-radius:30px;
  background-image:var(--glass-grad);
  border:1px solid var(--glass-border);
  -webkit-backdrop-filter:blur(26px) saturate(180%);backdrop-filter:blur(26px) saturate(180%);
  box-shadow:var(--rim),var(--drop);
}
.top-bar::before{
  content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(185deg,var(--top-light),rgba(255,255,255,0) 30%);
}
.brand{position:relative;z-index:1;display:flex;align-items:center;gap:12px;font-size:14px;font-weight:700;letter-spacing:.18em;color:var(--muted);}
.brand::before,.brand::after{content:'';width:48px;height:1px;background:currentColor;opacity:.4;}
.brand-dot{width:9px;height:9px;border-radius:50%;background:linear-gradient(135deg,#5ac8fa,#7d7aff 50%,#d678ff);box-shadow:0 0 10px rgba(125,122,255,.8);}

.level-bar{position:relative;z-index:1;display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:center;}
select{
  appearance:none;-webkit-appearance:none;
  padding:13px 46px 13px 22px;font-size:19px;font-weight:600;color:var(--ink);outline:none;cursor:pointer;
  border-radius:17px;border:1px solid var(--glass-border);
  background-color:transparent;
  background-image:var(--chev),var(--glass-grad);
  background-repeat:no-repeat,no-repeat;
  background-position:right 18px center,0 0;
  background-size:12px 8px,100% 100%;
  box-shadow:var(--rim),0 6px 18px -8px rgba(23,34,80,.3);
  -webkit-backdrop-filter:blur(18px) saturate(170%);backdrop-filter:blur(18px) saturate(170%);
  transition:box-shadow .25s,transform .25s;
}
select:hover{transform:translateY(-1px);}
select:focus{box-shadow:var(--rim),var(--focus);}

/* ---------- 模式切换：iOS 分段控件 ---------- */
.mode-bar{
  position:relative;z-index:1;display:flex;gap:4px;padding:5px;border-radius:999px;
  background:var(--seg-track);border:1px solid var(--seg-border);
  box-shadow:inset 0 2px 6px rgba(20,28,60,.10),inset 0 -1px 0 rgba(255,255,255,.25);
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
}
button{cursor:pointer;-webkit-tap-highlight-color:transparent;}
button:disabled{cursor:not-allowed;}
.mode-bar button{
  padding:11px 26px;border:none;border-radius:999px;background:transparent;color:var(--seg-ink);
  font-size:17px;font-weight:600;user-select:none;
  transition:all .28s cubic-bezier(.34,1.4,.64,1);
}
.mode-bar button:hover{color:var(--ink);}
.mode-bar button.mode-active{
  color:var(--ink);
  background:linear-gradient(165deg,rgba(255,255,255,.96),rgba(255,255,255,.72));
  box-shadow:0 3px 10px rgba(23,34,80,.18),inset 0 1px 0 #fff,inset 0 -1px 0 rgba(255,255,255,.6);
}
@media (prefers-color-scheme: dark){
  .mode-bar button.mode-active{
    color:#fff;
    background:linear-gradient(165deg,rgba(255,255,255,.22),rgba(255,255,255,.10));
    box-shadow:0 3px 10px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.3);
  }
}

/* ---------- 进度条 ---------- */
.progress-wrapper{
  width:100%;max-width:1200px;height:10px;border-radius:999px;background:var(--track);
  border:1px solid var(--track-border);
  box-shadow:inset 0 1px 3px rgba(20,28,60,.14),0 4px 14px rgba(23,34,80,.10);
  overflow:hidden;z-index:10;
  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
}
.progress-fill{
  height:100%;border-radius:999px;
  background:linear-gradient(90deg,#4fc3ff,#6d7bff 45%,#b06cff);
  box-shadow:0 0 14px rgba(109,123,255,.65),inset 0 1px 0 rgba(255,255,255,.55);
  transition:width .45s cubic-bezier(.4,0,.2,1);
}

/* ---------- 单词卡（翻转结构保持不变） ---------- */
.flip-container{
  perspective:6000px;width:92vw;max-width:1200px;--card-min-h:560px;
  cursor:pointer;z-index:10;-webkit-tap-highlight-color:transparent;
  transition:transform .45s ease;
}
.flip-container:hover{transform:translateY(-4px);}
.flipper{
  display:grid;width:100%;min-height:var(--card-min-h);
  transition:transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
  transform-style:preserve-3d;
}
.flip-container.flipped .flipper{transform:rotateY(180deg);}
.card-front,.card-back{
  grid-area:1/1;position:relative;isolation:isolate;overflow:hidden;
  width:100%;min-height:var(--card-min-h);
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
  border-radius:36px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:52px 46px;user-select:none;
  box-shadow:var(--drop);
}
.card-front{
  color:var(--ink);z-index:2;
  background-image:
    radial-gradient(130% 90% at 88% -12%,rgba(150,175,255,.32),transparent 52%),
    radial-gradient(120% 85% at -12% 112%,rgba(255,185,222,.25),transparent 48%),
    linear-gradient(165deg,rgba(255,255,255,.74),rgba(255,255,255,.44));
  -webkit-backdrop-filter:blur(30px) saturate(190%);backdrop-filter:blur(30px) saturate(190%);
  border:1px solid rgba(255,255,255,.65);
}
.card-back{
  color:#fff;transform:rotateY(180deg);z-index:1;
  background-image:
    radial-gradient(130% 90% at 88% -12%,rgba(124,142,255,.4),transparent 52%),
    radial-gradient(120% 85% at -12% 112%,rgba(255,120,205,.28),transparent 48%),
    linear-gradient(165deg,rgba(36,41,92,.75),rgba(20,23,56,.66));
  -webkit-backdrop-filter:blur(30px) saturate(170%);backdrop-filter:blur(30px) saturate(170%);
  border:1px solid rgba(255,255,255,.28);
}
/* 玻璃边缘：高光棱线 + 折射光环（液态玻璃的 signature） */
.card-front::before,.card-back::before{
  content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:4;
  box-shadow:
    inset 0 1.5px 1px rgba(255,255,255,.95),
    inset 0 -1.5px 1.5px rgba(255,255,255,.32),
    inset 1.2px 0 1px rgba(255,255,255,.5),
    inset -1.2px 0 1px rgba(255,255,255,.5),
    inset 0 0 34px rgba(255,255,255,.14);
}
/* 镜面高光：随指针流动的 specular（由脚本写入 --shx/--shy） */
.card-front::after,.card-back::after{
  content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:1;
  background:
    radial-gradient(620px circle at var(--shx,72%) var(--shy,6%),rgba(255,255,255,.32),transparent 44%),
    linear-gradient(198deg,rgba(255,255,255,.38) 0%,rgba(255,255,255,0) 26%);
}
.card-back::after{
  background:
    radial-gradient(620px circle at var(--shx,72%) var(--shy,6%),rgba(255,255,255,.20),transparent 44%),
    linear-gradient(198deg,rgba(255,255,255,.22) 0%,rgba(255,255,255,0) 28%);
}
.card-front>*,.card-back>*{position:relative;z-index:3;}

.progress-badge{
  position:absolute;top:18px;left:22px;z-index:20;
  font-size:16px;font-weight:700;letter-spacing:.03em;padding:7px 16px;border-radius:999px;
  color:#fff;background:rgba(21,26,58,.42);
  border:1px solid rgba(255,255,255,.30);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 6px 16px rgba(10,14,40,.28);
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
}

.main-text{font-size:clamp(36px,6vw,84px);font-weight:800;letter-spacing:-.015em;margin-bottom:14px;text-align:center;line-height:1.15;width:100%;overflow-wrap:break-word;word-break:break-word;}
.front-en-text{font-size:clamp(26px,4.5vw,52px);font-weight:700;color:var(--en-ink);margin-bottom:6px;text-align:center;line-height:1.25;width:100%;overflow-wrap:break-word;word-break:break-word;}
.front-ne-text{font-size:clamp(24px,4vw,46px);font-weight:600;color:var(--ne-ink);margin:4px 0;text-align:center;line-height:1.25;width:100%;overflow-wrap:break-word;word-break:break-word;}
.front-cn-text{font-size:clamp(26px,4.5vw,52px);font-weight:700;color:var(--cn-ink);margin-top:6px;text-align:center;line-height:1.25;width:100%;overflow-wrap:break-word;word-break:break-word;}
.hint{
  margin-top:24px;display:inline-flex;align-items:center;gap:8px;
  font-size:15px;font-weight:600;color:var(--muted);
  padding:9px 18px;border-radius:999px;
  background:rgba(94,108,160,.10);border:1px solid rgba(94,108,160,.16);
}

.back-main{font-size:clamp(36px,6vw,84px);font-weight:800;letter-spacing:-.015em;margin-bottom:10px;text-align:center;line-height:1.15;width:100%;overflow-wrap:break-word;word-break:break-word;}
.back-kana{
  font-size:clamp(24px,4vw,42px);color:#cfe0ff;margin:8px 0 16px;font-weight:600;
  padding:6px 22px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.18);border-radius:14px;
  max-width:100%;overflow-wrap:break-word;word-break:break-word;text-align:center;
}
.back-lang-block{width:100%;max-width:920px;display:flex;flex-direction:column;gap:10px;margin-top:10px;}
.lang-row{display:flex;justify-content:center;align-items:flex-start;gap:14px;flex-wrap:wrap;}
.lang-label{
  font-size:16px;font-weight:700;color:rgba(255,255,255,.92);
  background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.18);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2);
  padding:4px 12px;border-radius:9px;min-width:56px;text-align:center;flex-shrink:0;
}
.lang-value{font-size:clamp(20px,3.5vw,36px);font-weight:500;color:rgba(255,255,255,.96);line-height:1.35;text-align:center;max-width:100%;overflow-wrap:break-word;word-break:break-word;flex:1;min-width:0;}

/* ---------- 底部控制：玻璃胶囊按钮 ---------- */
.controls{
  display:flex;gap:14px;flex-wrap:wrap;justify-content:center;z-index:10;width:100%;max-width:1200px;
}
.controls button{
  position:relative;overflow:hidden;border-radius:999px;
  padding:15px 32px;font-size:19px;font-weight:700;color:var(--ink);
  border:1px solid var(--glass-border);
  background-image:var(--glass-grad);
  -webkit-backdrop-filter:blur(20px) saturate(180%);backdrop-filter:blur(20px) saturate(180%);
  box-shadow:var(--rim),0 10px 26px -10px rgba(23,34,80,.38);
  transition:transform .22s cubic-bezier(.34,1.56,.64,1),box-shadow .22s,opacity .2s;
  user-select:none;
}
.controls button::before{
  content:'';position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(185deg,rgba(255,255,255,.5),rgba(255,255,255,0) 40%);
}
.controls button:hover{transform:translateY(-2px);box-shadow:var(--rim),0 16px 34px -12px rgba(23,34,80,.5);}
.controls button:active{transform:scale(.95);}
.controls button:disabled{opacity:.55;transform:none;}
#shuffle{
  color:#0c7a5c;border-color:rgba(255,255,255,.55);
  background-image:linear-gradient(165deg,rgba(184,255,230,.78),rgba(146,238,202,.48));
}
#next{
  color:#fff;border-color:rgba(255,255,255,.38);
  background-image:linear-gradient(165deg,rgba(88,102,255,.95),rgba(128,94,255,.9));
  box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 12px 30px -10px rgba(92,102,255,.7);
}
#next::before{background:linear-gradient(185deg,rgba(255,255,255,.4),rgba(255,255,255,0) 45%);}
#next:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 18px 40px -12px rgba(92,102,255,.85);}
@media (prefers-color-scheme: dark){
  .controls button::before{background:linear-gradient(185deg,rgba(255,255,255,.16),rgba(255,255,255,0) 40%);}
  #shuffle{color:#8df2c8;background-image:linear-gradient(165deg,rgba(46,160,118,.5),rgba(30,120,90,.32));}
}

/* ---------- 页脚提示 ---------- */
.info{
  color:var(--muted);font-size:14.5px;font-weight:500;letter-spacing:.02em;z-index:10;
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center;
}
.kbd{
  display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:24px;padding:0 7px;
  border-radius:8px;font-size:12.5px;font-weight:700;color:var(--kbd-ink);
  background:var(--kbd-bg);border:1px solid var(--kbd-border);
  box-shadow:0 2px 4px rgba(20,28,60,.14),inset 0 -1.5px 0 rgba(20,28,60,.10);
}

/* ---------- 入场动画 ---------- */
.top-bar,.progress-wrapper,.flip-container,.controls,.info{animation:rise .7s cubic-bezier(.22,1,.36,1) backwards;}
.progress-wrapper{animation-delay:.06s;}
.flip-container{animation-delay:.12s;}
.controls{animation-delay:.18s;}
.info{animation-delay:.24s;}
@keyframes rise{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:none;}}

@media (prefers-reduced-motion: reduce){
  .orb{animation:none;}
  .top-bar,.progress-wrapper,.flip-container,.controls,.info{animation:none;}
  .flip-container:hover{transform:none;}
}

@media(max-width:600px){
  body{padding:16px 10px 26px;gap:16px;}
  .flip-container{--card-min-h:440px;}
  .card-front,.card-back{padding:30px 18px;border-radius:26px;}
  .top-bar{padding:14px 12px 16px;border-radius:24px;gap:12px;}
  select{font-size:17px;padding:11px 40px 11px 18px;}
  .mode-bar button{font-size:14px;padding:9px 16px;}
  .controls button{padding:12px 20px;font-size:16px;}
  .controls{gap:10px;}
  .progress-badge{top:12px;left:14px;font-size:14px;}
}
</style>
</head>
<body>

<div class="bg" aria-hidden="true">
  <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div><div class="orb o4"></div><div class="orb o5"></div>
</div>

<header class="top-bar">
  <div class="brand"><span class="brand-dot"></span>できる日本語　単語カード</div>
  <div class="level-bar">
    <select id="levelSelect">
      <option value="初級">初級</option>
      <option value="初中級">初中級</option>
      <option value="中級">中級</option>
    </select>
    <select id="lessonSelect"></select>
  </div>
  <div class="mode-bar">
    <button id="mode1" class="mode-active">漢字→読み・意味</button>
    <button id="mode3">英・中・ネパール語→日本語</button>
  </div>
</header>

<div class="progress-wrapper"><div class="progress-fill" id="progressFill"></div></div>

<div class="flip-container" id="cardWrap">
  <div class="flipper">
    <div class="card-front">
      <div class="progress-badge" id="progressBadge">1 / 45</div>
      <div class="main-text" id="frontMain"></div>
      <div class="front-en-text" id="frontEn"></div>
      <div class="front-ne-text" id="frontNe"></div>
      <div class="front-cn-text" id="frontCn"></div>
      <div class="hint">👆 クリック / タップで答えを表示</div>
    </div>
    <div class="card-back">
      <div class="progress-badge" id="backProgressBadge">1 / 45</div>
      <div class="back-main" id="backMain"></div>
      <div class="back-kana" id="backKana"></div>
      <div class="back-lang-block">
        <div class="lang-row"><span class="lang-label">EN</span><span class="lang-value" id="backEng"></span></div>
        <div class="lang-row"><span class="lang-label">中</span><span class="lang-value" id="backCn"></span></div>
        <div class="lang-row"><span class="lang-label">NE</span><span class="lang-value" id="backNe"></span></div>
      </div>
    </div>
  </div>
</div>

<div class="controls">
  <button id="prev">← 前へ</button>
  <button id="shuffle">🔀 シャッフル</button>
  <button id="next">次へ →</button>
</div>

<p class="info">
  <span class="kbd">Space</span>カード反転<span class="kbd">←</span><span class="kbd">→</span>単語移動・スワイプ：左右切替
</p>

'''

ENHANCER = r'''<script>
/* 液态玻璃增强：镜面高光跟随指针（不影响原有逻辑） */
(function(){
  var wrap = document.getElementById('cardWrap');
  if(!wrap || !window.matchMedia) return;
  if(!matchMedia('(pointer:fine)').matches) return;
  function set(x,y){ wrap.style.setProperty('--shx',x); wrap.style.setProperty('--shy',y); }
  wrap.addEventListener('pointermove', function(e){
    var r = wrap.getBoundingClientRect();
    set(((e.clientX-r.left)/r.width*100).toFixed(1)+'%', ((e.clientY-r.top)/r.height*100).toFixed(1)+'%');
  });
  wrap.addEventListener('pointerleave', function(){ set('72%','6%'); });
})();
</script>
</body>
</html>
'''

idx = s.index('<script>')
rest = s[idx:]
# rest 以 </script>\n</body>\n</html>(\n) 结尾：去掉旧收尾，换上新增强脚本
tail = '</script>\n</body>\n</html>'
assert rest.rstrip('\n').endswith(tail), 'unexpected tail: %r' % rest[-40:]
rest = rest.rstrip('\n')[:-len(tail)] + '</script>\n' + ENHANCER

out = MARKUP + rest
open(p, 'w', encoding='utf-8', newline='\n').write(out)
print('index.html 液态玻璃改版完成, 总长度:', len(out))
