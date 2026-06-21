# CLAUDE.md · 诺曼底碉堡

## 项目本质
单文件 HTML5 Canvas 像素射击游戏。所有代码在 `index.html` 内联(CSS + vanilla JS)。无构建、无依赖、无后端。

## 运行
```bash
# 任一静态服务器即可,或直接双击 index.html
python3 -m http.server 4178
# 打开 http://localhost:4178/index.html
```

## 代码地图(index.html 内)
- `AudioFX` — WebAudio 程序化音效(shoot/hit/kill/hurt/wave/supply/over)
- 输入层 — mouse/keys 事件,`onPrimary()` 统一处理开始/继续/开火
- 状态机 — `state ∈ {title, play, pause, over}`
- `reset() / startGame()` — 初始化英雄、碉堡血量、波次
- 波次系统 — `startWave() / spawnQueue / spawnEnemy()`
- `tryFire() / reload()` — 射击与换弹
- `update(dt)` — 主逻辑(移动/子弹/碰撞/敌人/补给/粒子/物理)
- `draw()` — 分层渲染(天空→海→沙滩→碉堡→敌人→英雄→弹壳→子弹→粒子→HUD→屏幕)
- `pxRect()` — 像素方块绘制 helper

## 调参锚点
- 难度:`startWave()` 里的 `count / baseHP / spd`
- 手感:`hero.fireRate`(开火间隔)、`sp=720`(子弹速度)、`shake`(震动)
- 平衡:`damageBunker()` 伤害、空投概率 `Math.random()<.7`

## 约定
- 改动后保持单文件;新增资源一律程序化绘制或内联。
- 验证用 Playwright 跑 http 服务器(file:// 被浏览器拦截)。
- 设计改动需过 impeccable 闸门(保持字体层级:展示字体 vs 正文等宽)。
