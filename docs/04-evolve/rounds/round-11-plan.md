# Round 11 · 全怪物动画 + 10 关 + 胜利过场/奖励(会议文案)
> 2026-06-20 · Alan · Workflow 并行资产 + 前台系统

## 需求
1. 所有怪物加动态走路动画(多生成图,动作逼真)。
2. 10 关结构,每关通关有 5s 胜利过场动画。
3. 通关 10 关 → 最终胜利动画 + 音乐。
4. 给玩家发奖励。

## 设计
### 全怪物动画(6 种 · 视频→序列帧管线)
runner/elite/brute/exploder/spitter/armored 各做图生视频走路循环→抽帧→自适应抠图→spritesheet(soldier 已有)。缺失/失败的回退静态+程序化步态。

### 10 关结构
- 每关 = 固定波数(关1=3波,逐关+1,关10=12波)+ 关末 BOSS 倾向(后期波加重型怪)。
- 关间 5s **胜利过场**:播放胜利 CG 视频(可复用 2 段轮换)+ "SECTOR N SECURED" banner + 奖励结算。
- 场景每关推进(滩头→夜袭→海堤 循环)。

### 奖励系统
- 每关通关:+分数奖励、补满弹药、修碉堡 +N、解锁提示;里程碑(第3/6/9关)解锁/强化。
- 通关 10 关:最终胜利 CG + Lyria 胜利乐 + 总结算(总分/总歼敌/评级 S/A/B)+ 奖励勋章。

### 资产(Workflow 并行)
| Track | 产出 |
|---|---|
| 6× 怪物走路动画 | assets/anim/zombie-{type}/walk-sheet-sm.png + dims |
| 关卡胜利过场 | assets/cutscene/victory-clip.mp4(5s) |
| 最终胜利 CG | assets/cutscene/final-victory.mp4 |
| 胜利音乐(Lyria) | assets/bgm/victory-theme.mp3(Alan 直出) |
| FX 帧(上轮 gpt-image-2) | flame/muzzle-gpt-sheet(整合中) |

## 系统(前台)
LEVELS 配置 + level/wave 双层进度 + 过场状态机(state:'cutscene')+ 胜利结算 + 奖励 + 最终胜利屏。资产缺失优雅降级(过场退化为 banner)。

## 验收
10 关可推进、每关过场+奖励、通关最终 CG+乐+评级、全怪物走动画、Playwright 实测无报错。
