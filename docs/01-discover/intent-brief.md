# Intent Brief · BLACKTIDE

> Project codename: `normandy-bunker-shooter` (legacy directory name)
> Shipped title: **BLACKTIDE · Siege of the Last Cape** — Cycle 9
> Owner: simprr@gmail.com · Last updated: 2026-06-21 (post r32)

---

## Primary Goal

构建一个**单文件 HTML 的电影化 2D 第一人称固定位 FPS**:玩家扮演 Last Cape 灯塔的最后守望者 **Marshal Eisen**,在第 9 轮百年黑潮(Black Tide Cycle 9)中独守一墙、一岬、一岸,顶住 10 个章节、两位 boss(Tidelord @ Lv5 / Leviathan @ Lv10)、约 5 分钟通关的不死浪潮。

r0 最初锚定为「Normandy 滩头掩体射击」,但 r15 起做了**世界观大切换**:剥离所有现实军事/国家符号(无米字旗 / 无星条旗 / 无 WW2 制服 / 无 Eisenhower 引用),转为 100% 虚构的「百年诅咒 × 中世纪石垒守望者」奇幻设定。r32 时项目已是一款完成度极高的 cinematic single-file shooter:

- 10 章 narrative arc + 每章独有 epigraph + Eisen 电报体语音
- 2 位 boss 多阶段战斗(HP 双倍化 + 3 phase 转阶段 + 8 帧 sprite sheet)
- 4 首 Gemini Lyria 真管弦乐 stems + WebAudio 5 IR 程序化混响
- 4K GPT-Image-2 photoreal 场景立绘 + PIL chroma-key alpha pipeline
- Pippit Seedance 生成的章节过场 mp4

## 用户故事 / 客户画像

- **客户类型**:个人项目(simprr 自玩 + 开源展示作品)
- **使用场景**:
  1. 本机双击 `index.html` 即可起玩,无 build / 无 npm install / 无 env
  2. GitHub 仓库 **PUBLIC** 开源,展示「单 HTML 文件做出 cinematic FPS」的工程范式
  3. Vercel 部署到 `*.vercel.app`,返回 200,任何人打开 URL 即玩
- **核心动机**:把「一晚上 vibe coding 出能打的 FPS」做到电影级质感,作为 portfolio
- **非目标受众**:不面向多人对战 / 不面向手游 / 不面向商业发行

## 范围内(In Scope)

- 单 HTML 文件,内联 ~1914 行 vanilla JS,Phaser 3.80.1 via CDN
- 10 关固定关卡 + 2 boss 战 + cinematic 开场/章节/过场/胜利序列
- Marshal Eisen 电报体台词系统(Courier typeface + typewriter SFX)
- 程序化 WebAudio 武器 / 怪物 / boss / 环境音效 + Lyria 真乐 BGM
- 5 个场景立绘(Last Cape Dawn / Black Cove Flares / Sandbag Trench / Iron Seawall / Cathedral Ruins)
- GitHub PUBLIC 仓库 + Vercel preview/production 部署
- Playwright 实测脚本:启动 → 通关 → 0 console error

## 范围外(Out of Scope)

- 多人 / 联网 / 排行榜 / 账号系统
- 移动端触屏适配(仅鼠标 + 键盘桌面端)
- 任何现实国家符号、WW2 / Normandy / Eisenhower 文化引用
- 任何需要后端的功能(无数据库 / 无 API / 无登录)
- 二次构建工具链(无 Webpack / Vite / TypeScript / 任何 npm 依赖)
- 内购 / 商业化 / DRM

## 成功指标

| # | 指标 | 验收口径 |
|---|---|---|
| 1 | **5 分钟通关** | 从 START 到 Cycle 9 holds 字幕,熟练玩家 < 5 min |
| 2 | **10 关完整** | I·THE FIRST TOLL → X·LEVIATHAN 全部可达,boss 两阶段触发正确 |
| 3 | **Playwright 实测** | headless 启动 → 模拟射击通关 → 退出 console 0 error / 0 warning |
| 4 | **GitHub PUBLIC** | 仓库可访问,README 含截图 + 玩法 + tech stack |
| 5 | **Vercel 200** | production URL `curl -I` 返回 HTTP 200,首屏加载 < 3s |
| 6 | **资产同源** | Leviathan 8 帧 sprite 通过 GPT-Image-2 `--image-urls` 锁定身份一致 |
| 7 | **音乐就位** | 4 首 Lyria stem(battle/boss/title/victory)真乐文件本地化,无 404 |

## 约束

- **单文件 HTML 硬约束**:所有逻辑 / 样式 / 数据 inline 进 `index.html`,资产以相对路径引用(`/assets/...`)
- **Phaser 3.80.1 via jsDelivr CDN**:不本地 bundle,不引入其他游戏框架(no PixiJS / no Three.js / no Babylon)
- **不引外部 JS 框架**:无 React / Vue / Svelte;纯 vanilla JS
- **5 分钟通关硬约束**:关卡时长 / 怪物 HP / boss 阶段触发点都以「熟练玩家 5 min 通关」反推平衡
- **WebGL 必需**:Phaser preFX glow / blend mode 依赖 WebGL,不做 Canvas fallback
- **桌面端 only**:鼠标瞄准 + 左键开火 + R 装弹 + Space 跳过 cutscene
- **资产合法性**:所有图像由 GPT-Image-2 生成 / 所有音乐由 Gemini Lyria 生成 / 所有视频由 Pippit Seedance 生成,无第三方版权素材
- **No-go themes**:绝不出现现实国旗、纹章、WW2 imagery、真实军服、现代军械 —— 任何 r15 前残留符号必须清除
