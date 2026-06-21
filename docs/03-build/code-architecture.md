# Code Architecture · BLACKTIDE index.html

> 单文件 HTML 架构剖析 · `BLACKTIDE · Siege of the Last Cape · Cycle 9` · ~1914 行 vanilla JS。
> 无 build / 无 bundler / 无 npm install / 无 env vars。打开 index.html 即玩。

---

## 1. 顶层结构

整个游戏是一个 `index.html`，按文档顺序自上而下分三段：

```
<!DOCTYPE html>
<html>
  <head>
    <meta …>
    <title>BLACKTIDE · Siege of the Last Cape</title>
    <style> … 全部样式（~250 行） … </style>
  </head>
  <body>
    … overlay 容器（title / chapter / epigraph / cutscene / pause / over / eisen） …
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
    <script>
      (() => {
        // AudioFX module-level IIFE state
        // 数据驱动 const（SCENES / CHAPTERS / EPIGRAPHS / TYPES / WEAPONS / EISEN_LINES / SCENE_AC / WALK_SHEETS）
        // class Battle extends Phaser.Scene { … }
        // new Phaser.Game({ scene: [Battle], … });
      })();
    </script>
  </body>
</html>
```

设计原则：

- **零依赖加载**：Phaser 3.80.1 走 jsDelivr CDN，其余全部 inline。
- **三段切片**：CSS（呈现）、HTML overlay（UI 元素静态骨架）、JS IIFE（行为）—— 互不污染全局。
- **IIFE 隔离**：脚本全部包裹在 `(() => { … })()` 内，仅 `window.Phaser` 是外部符号。

---

## 2. CSS 层

CSS 集中在 `<head><style>` 中，遵循「通用 + 各 overlay 自配色」的两层结构。

### 2.1 通用基底

- `html, body` —— 满屏黑、`overflow:hidden`、禁止文本选中、`touch-action:none`。
- `#game` —— Phaser canvas 挂载点，绝对定位铺满，z-index 0。
- `.overlay` —— 通用浮层基类：`position:absolute; inset:0; display:flex;` 居中、半透明黑底、`pointer-events:auto`、`z-index:10+`。
- 字体栈：`--display: 'Black Ops One', sans-serif` 作为标题（Google Fonts import）；`--body: 'Oswald', sans-serif` 作为副标 / epigraph / 武器名；Eisen 电报 epigraph lede 用 `'Courier New', monospace`。**无 Cinzel**。与 `docs/02-design/design-system.md §1` 同源。

### 2.2 各 overlay 配色（每个 ID 独立 palette）

| ID | 用途 | 主色调 | 关键效果 |
|---|---|---|---|
| `#title` | 标题屏 | 深海蓝 #0a1620 + 锈红 #c8503c | 大号 Black Ops One 标题、字间距开 8px、副标 Cycle 9 闪烁 |
| `#chapter` | 章节卡 | 纯黑 + 暖白 #f0e7d8 | 罗马数字大写、`letter-spacing: 12px`、淡入 600ms（Black Ops One display） |
| `#epigraph` | 题词卡 | 半透明黑 + 米黄 #e6dcc0 | Courier New 引言体、限宽 720px、底部署名 `— Marshal Eisen` |
| `#cutscene` | 过场视频 | 黑底 + `<video>` 满屏 | 可跳过提示右下角 |
| `#pause` | 暂停菜单 | #11181f + #8aa0b0 | RESUME / RESTART / QUIT 三按钮、键盘 P 切换 |
| `#over` | 失败/胜利 | 失败用 #2a0808 + 血红；胜利用 #08200a + 烛金 | 大字「HOLD BROKEN」/「CYCLE 9 HOLDS」 |
| `#eisen` | Eisen 字幕带 | 半透明黑横条 + Courier 米色 + 左侧 portrait 84x84（r30 落地尺寸,与 design-system §3 同源） | 头像在 BOSS phase 切换时 `filter: hue-rotate + saturate(2)` 闪红 |

### 2.3 动效

- `@keyframes typewriterCaret` —— Courier 字幕末尾光标。
- `@keyframes flickerCycle9` —— 标题屏副标轻闪。
- `@keyframes redPulse` —— Eisen portrait BOSS 红闪。
- 所有 overlay `transition: opacity 420ms ease` 用于 JS 切 `.visible` class。

---

## 3. HTML overlay 骨架

`<body>` 内静态声明所有浮层，JS 通过切 `class="overlay visible"` 显示。

```html
<div id="game"></div>

<div id="title" class="overlay">
  <h1>BLACKTIDE</h1>
  <h2>Siege of the Last Cape</h2>
  <p class="cycle">— Cycle 9 —</p>
  <button id="start">HOLD THE LINE</button>
</div>

<div id="chapter" class="overlay">
  <div class="roman">I</div>
  <div class="name">THE FIRST TOLL</div>
  <div class="sub">Bell tower, third toll. They are walking.</div>
</div>

<div id="epigraph" class="overlay">
  <blockquote id="epigraph-text">…</blockquote>
  <div class="sig">— Marshal Eisen, Cycle 9</div>
</div>

<div id="cutscene" class="overlay">
  <video id="cutscene-video" playsinline></video>
  <div class="skip">SPACE to skip</div>
</div>

<div id="pause" class="overlay">
  <button data-act="resume">RESUME</button>
  <button data-act="restart">RESTART</button>
  <button data-act="quit">QUIT TO TITLE</button>
</div>

<div id="over" class="overlay">
  <h1 id="over-title">HOLD BROKEN</h1>
  <p id="over-stats">…</p>
  <button id="over-retry">AGAIN</button>
</div>

<div id="eisen" class="eisen-band">
  <img id="eisen-portrait" src="assets/eisen-portrait.png">
  <div id="eisen-text">…</div>
</div>
```

字幕带 `#eisen` 是常驻显示但默认空文本；BOSS phase shift 时给 `#eisen-portrait` 加 `.red-pulse` class。

---

## 4. AudioFX 模块

`AudioFX` 是脚本最上方的 module-level IIFE（`const AudioFX = (() => { … return {…}; })()` 在 index.html L225 起），集中管理 WebAudio + Lyria BGM 元素引用。**所有导出都 flat 挂在 `AudioFX` 对象上**，**没有** `SFX.*` / `BGM.*` 子命名空间。

### 4.1 核心 const（一次性初始化）

```js
let ac = null;                     // lazy AudioContext，首次 ensure() 时创建
let _masterLP, _masterGain;        // master lowpass + master gain
let _reverb, _reverbGain;          // 程序化 IR reverb (默认 1.8s) + wet gain
let _ambSource, _ambGain;          // 当前场景 ambience noise loop + gain
// 信号链: source → [panner] → _masterLP → _reverb(wet) ↘
//                                              ↘     _masterGain → destination
// 受用户手势驱动: ensure() 在首次音效调用里 new AudioContext + resume()
```

### 4.2 导出 API（全部 flat 挂在 `AudioFX` 上，签名按 index.html L581-633 的 return 块）

| 方法 | 用途 |
|---|---|
| `setMasterVolume(v)` / `setMuted(b)` / `getMasterVolume()` / `getMuted()` / `_applyVol()` | 主音量与静音持久化（localStorage 同步） |
| `setWorldWidth(w)` / `panTo(a, x)` | 设置世界宽（默认 1280）后，按敌人/事件 x 坐标插入 `StereoPannerNode`，未传 x 则透传 bus |
| `setSceneAcoustic(idx)` | **入参是 int 索引 0..4**（不是 `'cathedral'` 这种 key），切换 IR + ambience bed + wet level |
| `stopSceneAmbience()` | 淡出当前 ambience loop |
| `diveIn()` / `diveOut()` | 慢镜专用：lowpass 砍到 620Hz + BGM duck / 还原 |
| `shot(x)` / `shotgun(x)` / `rifle(x)` / `flame(x)` | 4 把武器各自合成枪声（按 WEAPONS[*].sfx 字符串调度） |
| `dry()` / `reload()` / `reloadDone()` / `lowAmmoTick()` | 空仓 / 装填 / 装填完成 / 低弹提示 |
| `hit(x)` / `kill(x)` / `headshot()` | 杂兵击中 / 死亡 / 爆头脆响 |
| `hurt()` | 玩家受伤 |
| `bossRoar(type, x)` | `'tidelord'` / `'leviathan'` 不同 sub + formant 配方 |
| `bossHit(x)` / `bossPhase(x)` / `bossDeath(type)` | BOSS 被击中金属铛 / 阶段切换 80→26Hz sub-drop + chirp / 终结长 sub-drop |
| `roar(type, x)` | 杂兵咆哮（4 体型预设：runner / soldier / elite / brute） |
| `telegraphDit()` / `heartbeat()` | Eisen 电报字符 tick / 低血心跳脉冲（程序化合成） |
| `levelStinger()` / `bossStinger()` | 章节通关 C-E-G 三连音 / BOSS 击败 1.3s 重低音管弦 |
| `ammoPickup()` / `healPickup()` / `boostPickup()` | 拾取反馈三件套 |
| `startBGM()` / `stopBGM()` | 程序化氛围 BGM（drone + 慢战鼓 + 远炮），与 Lyria MP3 互补 |
| `bgmCrossfade(fromEl, toEl, fromVol, toVol, ms)` | Lyria MP3 stem 之间淡入淡出（操作 `<audio>` element） |
| `wave()` / `supply()` / `thunder()` / `over()` | 波次提示 / 补给 / 远雷 / Game Over 跌音 |

> **不存在的 API**（先前文档错列）：`SFX.shoot` / `SFX.zombieHit` / `SFX.zombieDie` / `SFX.bellToll` / `SFX.typewriter` / `BGM.play` / `BGM.duck` 全部为虚构命名空间；钟声与打字机分别由 page-level Howler 实例 / `telegraphDit` 程序合成承担。

### 4.3 数据：`SCENE_AC`（5 元素数组,L247-253）

```js
const SCENE_AC = [
  // idx 0 beach 开阔海岸
  { irLen:1.8, decay:2.2, wet:0.18, ambFreq:280,  ambQ:0.4, ambGain:0.10 },
  // idx 1 night/cove 雾闷
  { irLen:1.4, decay:1.8, wet:0.22, ambFreq:140,  ambQ:0.6, ambGain:0.11 },
  // idx 2 seawall 石回响
  { irLen:2.4, decay:2.6, wet:0.28, ambFreq:1800, ambQ:0.3, ambGain:0.08 },
  // idx 3 trench 泥水沉
  { irLen:1.0, decay:1.6, wet:0.15, ambFreq:180,  ambQ:0.5, ambGain:0.09 },
  // idx 4 ruins 大教堂
  { irLen:3.2, decay:2.8, wet:0.34, ambFreq:520,  ambQ:0.4, ambGain:0.12 },
];
```

字段含义：`irLen` IR 长度（秒）；`decay` 衰减指数；`wet` reverb wet 输出比；`ambFreq/ambQ/ambGain` ambience noise bed 的 lowpass 中心频率 / Q / 增益。`setSceneAcoustic(idx)` 按 idx 重建 `_reverb.buffer` 程序化 IR 并 crossfade ambience noise loop（约 1.2s）。**没有 `lp` / `irPreset` 字段**，也没有按 key 索引的对象映射。

---

## 5. `class Battle extends Phaser.Scene`

`new Phaser.Game({ scene:[Battle], … })` 只注册了这一个 Scene；标题屏 / 章节卡 / 题词 / 暂停 / Game Over 都是 DOM overlay 由 Battle 通过切 `.visible` class 控制（**没有** BootScene / TitleScene / BattleScene / HudOverlay 等额外 class）。方法按生命周期分组：

### 5.1 生命周期方法

| 方法 | 职责 |
|---|---|
| `preload()` | 加载 5 个 scene 背景、敌人静态 + walk sprite sheet、Eisen portrait、Leviathan 8 帧多角度表、武器 FP 贴图、4 个 BGM stem、cutscene mp4 |
| `create()` | 初始化 HUD overlay（弹药 / HP / 分数 / 章节）、武器组、敌人池、boss 占位、绑定 input（鼠标瞄准、左键开火、1/2/3/4 换武器、R 装填、P 暂停、SPACE 跳过 cutscene）、`time.delayedCall` 注册 Eisen 字幕队列 |
| `update(t, dt)` | 每帧推进：敌人 AI（朝玩家爬）、boss 行为机 tick、武器冷却、HUD 数值同步、wave spawn 调度、**phase shift 检测 inline 在此**（达 HP 阈值时直接调用 `AudioFX.bossPhase(x)` + edgePulse + 召唤 runners，不经独立方法） |

### 5.2 流程方法（按 index.html 实际签名）

| 方法 | 职责 |
|---|---|
| `showEpigraph(level, mode)` | 返回 Promise；显示 `#epigraph` 4s 可 SPACE 跳过；带 `_epigraphAbort` flag |
| `showEisenLine(key, …)` | 字幕浮层逐字渲染 + `telegraphDit` 程序合成音；**不是** `pushEisen` |
| `levelComplete()` / `finalVictory()` | 章节通关 / 终幕：替代旧文档里假想的 `endChapter(win)` / `showGameOver(win)`；分别播 `levelStinger` 和 `bossStinger` + 切 DOM overlay `#over` 的 win/lose 文案 |
| `spawn(type, opts)` | 在屏外远端实例化敌人 / boss；`opts` 含 lane / boss 标记等；**不是** `spawn(type, lane)` |
| `hitAt(px, py, w)` | 武器命中判定按像素坐标 + 当前武器 `w` 算 spread / pellets / dmg，再调 `AudioFX.hit(x)` + `panTo`；**不是** `hitAt(x01)` |
| `hurtBunker(d)` | 玩家受伤入口（扣 bunkerHP）；**不是** `onPlayerHit(dmg)` |
| 击杀 / phase shift 逻辑 | 全部 inline 在 `update()` 中：达 HP 阈值直接屏震 + edgePulse + `bossPhase(x)` + summon runners + 红 portrait；不存在独立 `onKill` / `onBossPhaseShift` |
| 暂停 / 恢复 | `pauseGame()` / `resumeGame()` 切 `#pause` overlay |

---

## 6. 数据驱动 const

所有「内容」抽出为顶层常量，便于配平。

### 6.1 `SCENES`（数组,L658-664;按索引 `sceneIdx` 引用,与 `SCENE_AC[idx]` 同序）

```js
const SCENES = [
  { key:'bg',         name:'Last Cape · Dawn',         tint:0xcfd8da }, // 0
  { key:'bg_night',   name:'Black Cove · Flares',      tint:0xb8c0d8 }, // 1
  { key:'bg_seawall', name:'Iron Seawall · Fog',       tint:0xc8d2d4 }, // 2
  { key:'bg_trench',  name:'Sandbag Trench · Dusk',    tint:0xc6cfd8 }, // 3
  { key:'bg_ruins',   name:'Cathedral Ruins · Vigil',  tint:0xc8c0bc }, // 4
];
```

`CHAPTERS[level].sceneIdx` 引用该数组下标，同 idx 也对应 `SCENE_AC[idx]` 的声学预设。**不是** `{ dawn:{…}, cove:{…} … }` 这种对象映射。

### 6.2 `CHAPTERS`（10 条，对应世界书 ten_chapter_arc）

```js
const CHAPTERS = [
  { level: 1,  name: 'I · THE FIRST TOLL',            sub: 'Bell tower, third toll. They are walking.', scene: 'dawn'      },
  { level: 2,  name: 'II · BLACK TIDE RISES',         sub: 'Tide at +2m. Cycle 9, hour one.',           scene: 'dawn'      },
  { level: 3,  name: 'III · THE DROWNED MARCH',       sub: 'Signal flare seven. The cove answers.',     scene: 'cove'      },
  { level: 4,  name: 'IV · TRENCH OF ECHOES',         sub: 'Mud to the knees. The dead don\'t slow.',   scene: 'trench'    },
  { level: 5,  name: 'V · THE TIDELORD WAKES',        sub: 'Cycle 9 always breaks here. Not today.',    scene: 'seawall', boss: 'tidelord'  },
  { level: 6,  name: 'VI · CATHEDRAL OF THE DEAD',    sub: 'The chapel bell still hangs. Barely.',      scene: 'cathedral' },
  { level: 7,  name: 'VII · STORM VIGIL',             sub: 'Lightning every fifteen seconds. Count.',   scene: 'cove'      },
  { level: 8,  name: 'VIII · WHISPERS FROM THE DEEP', sub: 'Hour nine. The sea is louder than rifle.',  scene: 'seawall'   },
  { level: 9,  name: 'IX · THE FINAL BEACH',          sub: 'One wall. One marshal. One hundred years.', scene: 'dawn'      },
  { level: 10, name: 'X · LEVIATHAN OF THE BLACK TIDE',sub:'Hundred-year tide, last shore, last shot.', scene: 'cathedral', boss: 'leviathan' },
];
```

### 6.3 `EPIGRAPHS` —— 10 条题词字符串（与上文世界书 epigraph 字段一一对齐）。

### 6.4 `TYPES` —— 敌人原型（7 杂兵 + 2 boss,L634-646）

```js
const TYPES = {
  soldier:  { tex:'z_soldier',  hp:3,  speed:0.058, dmg:8,  score:10, nearH:300, … },
  runner:   { tex:'z_runner',   hp:2,  speed:0.110, dmg:6,  score:16, nearH:250, … },
  elite:    { tex:'z_elite',    hp:7,  speed:0.050, dmg:13, score:34, nearH:330, … },
  brute:    { tex:'z_brute',    hp:16, speed:0.032, dmg:24, score:70, nearH:460, … },
  exploder: { tex:'z_exploder', hp:4,  speed:0.078, dmg:0,  score:30, nearH:300, behavior:'explode' },
  spitter:  { tex:'z_spitter',  hp:5,  speed:0.052, dmg:0,  score:32, nearH:300, behavior:'ranged', stopAt:0.60, fireEvery:2.0 },
  armored:  { tex:'z_armored',  hp:30, speed:0.030, dmg:22, score:85, nearH:430, behavior:'armored' },
  tidelord: { tex:'z_boss_tidelord',  hp:180, speed:0.022, dmg:35, score:600,  nearH:520, boss:true, bossName:'TIDELORD' },
  leviathan:{ tex:'z_boss_leviathan', hp:320, speed:0.018, dmg:45, score:1200, nearH:600, boss:true, bossName:'LEVIATHAN OF THE BLACK TIDE' },
};
```

每个 type 还含 `walkKey` / `walkAnim`（指向 `WALK_SHEETS`）、`step` / `rock` / `bob`（程序化步态）、`tint`。**没有 `walker` 兵种**。每场出怪用 `WAVE_PRESETS[level]` 按概率 / 滚动 schedule 出。

### 6.5 `WEAPONS`（数组,L651-656;数字键 1-4 / 滚轮按 index 切换）

```js
const WEAPONS = [
  { id:'mg',      name:'MG-42 Machine Gun', tex:'gun_fp',      fireRate:80,  dmg:1,   headMul:2, pellets:1, spread:0,  clip:180, reloadDur:2.4, auto:true,  sfx:'shot',    recoil:1,   scaleW:0.66 },
  { id:'shotgun', name:'Trench Shotgun',    tex:'gun_shotgun', fireRate:620, dmg:1,   headMul:2, pellets:8, spread:78, clip:8,   reloadDur:2.0, auto:false, sfx:'shotgun', recoil:3.2, scaleW:0.62 },
  { id:'rifle',   name:'Sniper Rifle',      tex:'gun_rifle',   fireRate:780, dmg:5,   headMul:3, pellets:1, spread:0,  clip:10,  reloadDur:2.7, auto:false, sfx:'rifle',   recoil:4,   scaleW:0.60 },
  { id:'flamer',  name:'Flamethrower',      tex:'gun_flamer',  fireRate:45,  dmg:0.6, headMul:1, pellets:1, spread:0,  clip:320, reloadDur:3.2, auto:true,  sfx:'flame',   recoil:0.4, scaleW:0.64, flame:true },
];
```

字段含义：`fireRate` 是 ms-per-shot（**不是 RPM**）；`clip` = 弹匣 / 总弹药容量；`pellets`+`spread` 控制散射（shotgun 8 弹丸 78° 散布）；`headMul` 爆头倍率；`recoil` 后坐；`scaleW` 是 FP 贴图屏占比。**没有 `smg` / `rocket`**，没有 `splash` 字段，没有 `rpm`，没有 `key`（按数组 index 0-3 + 数字键 1-4 映射）。

### 6.6 `EISEN_LINES` —— 章节开场 10 句 + boss_entrance 2 句 + low_health 3 句 + final_victory 1 句，全部来自世界书 sample_lines。

### 6.7 `WALK_SHEETS` —— 7 杂兵 walk sheet 元数据（数组,L722-730）

```js
const WALK_SHEETS = [
  { key:'z_soldier_walk',  file:'assets/anim/zombie-soldier/walk-sheet-sm.png',  fw:240, fh:323 },
  { key:'z_runner_walk',   file:'assets/anim/zombie-runner/walk-sheet-sm.png',   fw:200, fh:269 },
  { key:'z_elite_walk',    file:'assets/anim/zombie-elite/walk-sheet-sm.png',    fw:200, fh:269 },
  { key:'z_spitter_walk',  file:'assets/anim/zombie-spitter/walk-sheet-sm.png',  fw:200, fh:271 },
  { key:'z_armored_walk',  file:'assets/anim/zombie-armored/walk-sheet-sm.png',  fw:200, fh:410 },
  { key:'z_brute_walk',    file:'assets/anim/zombie-brute/walk-sheet-sm.png',    fw:200, fh:276 },
  { key:'z_exploder_walk', file:'assets/anim/zombie-exploder/walk-sheet-sm.png', fw:200, fh:269 },
];
```

Leviathan 8 帧多角度表是 BOSS 独立资产（`leviathan-anim-sheet.png`，r28 落地，r31 ledger 列为 4 关键 asset 之一），不在 `WALK_SHEETS` 内，由 `preload()` 单独 `load.spritesheet` 加载。Tidelord 是单贴图 `z_boss_tidelord`，**没有多帧表**。

---

## 7. 行为机模式（boss anim baseline + override + until 时钟）

Boss 不用 Phaser anim system，而是一个简单的「baseline + event override」状态机：

```js
boss._anim = {
  baseline: ['idle','idle_b'],  // 默认在两帧之间 800ms 振荡
  current : 'idle',
  override: null,               // 例: 'hurt'
  until   : 0,                  // performance.now() ms
};

function setBossOverride(frameName, durMs) {
  boss._anim.override = frameName;
  boss._anim.until    = performance.now() + durMs;
}

// 事件触发时长
hurt:        220 ms
slash_left:  320 ms
slash_right: 320 ms
roar:        420 ms
phase2_rage: 1500 ms（强制覆盖，phase shift 入场用）

// 每帧 update()
function tickBossAnim(now) {
  if (boss._anim.override && now < boss._anim.until) {
    boss.setFrame(frameIndex[boss._anim.override]);
  } else {
    boss._anim.override = null;
    const i = Math.floor(now / 400) % boss._anim.baseline.length;
    boss.setFrame(frameIndex[boss._anim.baseline[i]]);
  }
}
```

设计要点：

- **baseline 永远在跑**，事件 override 只是短暂打断。
- **until 时钟** 用 `performance.now()` 而非 dt 累计，避开 pause/blur 漂移。
- **phase2_rage** 是 phase shift 时强制 override 1500ms，配合 white-flash + radial shockwave + red phaseVig，制造演出节拍。

Tidelord 没有多角度表，只在 `idle / hurt / roar` 三态切换，复用同机器。

---

## 8. 状态机

游戏顶层是 6 状态线性图，由 `this._state` 字段驱动：

```
title ──► chapter ──► epigraph ──► (cutscene?) ──► play ──┐
                                                          │
            ┌───────────────── win  ◄── level=10 boss kill┤
            │                                             │
            └───────────────── over ◄── HP <= 0 ──────────┘

  play ──► chapter（next level）        // 完成当前 wave 序列
  play ◄►  pause（P 键，覆盖态）
```

### 8.1 关键 flag

| flag | 用途 |
|---|---|
| `_state` | 当前状态：`'title' \| 'chapter' \| 'epigraph' \| 'cutscene' \| 'play' \| 'pause' \| 'win' \| 'over'` |
| `_bossHpEntering` | 进入 boss wave 时锁定 HP UI 显示形态（出现 boss 血条），避免章节切换瞬间错位 |
| `_epigraphAbort` | 题词显示中按 SPACE 提前结束，避免 timer 仍在跑导致下一态被覆盖 |
| `_currentLevel` | 1..10 |
| `_currentWave` | 当前章节内的波次索引 |

### 8.2 转移规则

- `title → chapter`：点 HOLD THE LINE 按钮，`startLevel(1)`。
- `chapter → epigraph`：`chapter` 显示 1500ms 后自动转。
- `epigraph → cutscene`：仅当 `level ∈ {5, 10}` 且对应 `cut-boss5.mp4 / cut-boss10.mp4` 存在。
- `epigraph → play`：默认转入，开始 wave spawn。
- `cutscene → play`：视频 ended 或 SPACE 跳过。
- `play → chapter`：本章节最后一波清空 + boss 死亡（如有）后，`startLevel(level+1)`。
- `play → win`：level=10 + leviathan 死亡 → 播 victory BGM + Eisen 终句 `Cycle 9 holds.`。
- `play → over`：HP ≤ 0，停 BGM，显示失败 overlay。
- `play ↔ pause`：P 键互切，pause 不卸载场景。

---

## 9. 文件清单回顾

```
index.html                              单文件入口（~1914 行）
assets/
  bg.png / bg_night / bg_seawall /
  bg_trench / bg_ruins                  5 个场景背景（GPT-Image-2 4K + PIL chroma-key）
  zombie-soldier.png / zombie-runner / 
  zombie-elite / zombie-brute /
  zombie-spitter / zombie-armored /
  zombie-exploder.png                   7 杂兵静态贴图
  anim/zombie-*/walk-sheet-sm.png       7 杂兵 walk sprite sheet（详见 6.7）
  leviathan-anim-sheet.png              Leviathan BOSS 8 帧多角度表（360×360 per cell;r28/r31 ledger 关键 asset）
  z_boss_tidelord.png                   Tidelord BOSS 单贴图（**无** 多帧表）
  eisen-portrait.png                    字幕带头像（84×84,r30 落地）
  gun-fp.png / gun-shotgun / gun-rifle /
  gun-flamer                            4 把武器 FP 贴图
  cut-boss5.mp4                         Tidelord 入场（Seedance_2.0_mini）
  cut-boss10.mp4                        Leviathan 入场
  music/bgm-battle.mp3                  Lyria battle-theme
  music/bgm-boss.mp3                    Lyria boss-theme
  music/bgm-title.mp3                   Lyria title-theme
  music/bgm-victory.mp3                 Lyria victory-theme
```

打开 `index.html` 即玩，无构建步骤。
