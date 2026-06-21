---
name: game-core
description: 诺曼底碉堡的核心玩法循环规格——固定机位波次防守射击的状态机、波次系统、射击/换弹、碰撞与计分、补给与碉堡血量。改动玩法时以本文为准。
version: 1.0.0
allowed-tools:
  - Read
  - Edit
---

# game-core · 核心玩法规格

## 状态机
`title → play ⇄ pause → over → title`
- title:点击/空格 → `startGame()`
- play:`update(dt)` 驱动;P 暂停
- over:碉堡血量 ≤ 0;点击/空格回 title

## 波次循环
1. `betweenWave` 整备(2.5–3.5s)→ `startWave()`
2. `startWave()`:`count = 4 + floor(wave*1.6)`,`baseHP = 2 + floor(wave/3)`,`spd = 14 + wave*1.4`
3. 按 `spawnQueue[].delay` 逐个 `spawnEnemy()`
4. 队列空且无存活敌人 → 回到整备,70% 概率 `dropSupply()`
5. 精英敌:wave≥3 时按概率出现,3× 血量、0.7× 速度、5× 分。

## 射击
- `tryFire()`:消耗 1 弹药,冷却 = `fireRate/1000`(130ms),生成子弹(速度 720,微抖动)+ 弹壳 + 枪口粒子 + 震动。
- 弹药 ≤ 0 → 空仓音 + 自动 `reload()`。
- `reload()`:0.9s,补满弹匣(8)。

## 碰撞与计分
- 子弹 vs 敌人:AABB 近似,命中扣 1 血 + 白闪 + 血花。
- 击杀:`combo++`、`pts = (elite?50:10) * (1 + floor(combo/5))`、爆开粒子。
- combo 2.2s 不补击则清零。

## 碉堡血量
- 敌人 `x ≤ BUNKER_X+50` 触发攻击,每 0.9s 扣 3(精英 6)+ 震动。
- 血空 → `gameOver()`,写 `localStorage.nbs_best`。

## 补给
- `ammo` 补满弹药;`heal` 修复碉堡 +25。降落伞落地后 9s 内可拾取。

## 不变量
- 单文件、程序化绘制、无外部资源。
- dt 上限 0.05s。
- 改难度只动 `startWave()` 三参数与 `damageBunker()`,不破坏状态机。
