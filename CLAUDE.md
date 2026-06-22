# CLAUDE.md · BLACKTIDE · Siege of the Last Cape

> Cycle 9 — Marshal Eisen 在 Last Cape 灯塔守一墙、一岬、一岸,抵御百年涌起的 Black Tide 亡潮。

## 项目本质

单文件 HTML 的电影化 2D 第一人称定点 FPS。Phaser 3.80.1 + 纯 WebAudio + 单 `index.html`(~1914 行)。10 章节剧情弧,2 个 BOSS(Tidelord / Leviathan),无构建链、无 npm install,打开即跑。

## 运行 / 测试

```bash
# 本地:任何静态服务器即可
python3 -m http.server 8000        # → http://localhost:8000
# 或
npx serve .

# 部署:推到 main,Vercel 自动重发(vercel.json 已配)
git push origin main

# Playwright 验证:scripts/verify-*.mjs(若存在)
node scripts/verify-bossfight.mjs
```

## 代码地图(`index.html` 内)

| 区段 | 说明 |
|---|---|
| `<head>` CDN + 内联 CSS | Phaser 3.80.1 jsDelivr,Courier 字体,red phaseVig |
| `const SCENES = {...}` | 5 个场景配置(背景/远雾/近雾/光柱/音色) |
| `const CHAPTERS = [...]` | 10 章节定义(name/sub/scene/epigraph/boss?) |
| `const TYPES = {...}` | 敌人类型表(runner/brute/tidelord/leviathan) |
| `const WEAPONS = {...}` | 武器:rifle/shotgun/lmg(damage/recoil/spread/ammo) |
| `const EISEN_LINES` | Eisen 电报台词池(开章/BOSS/低血/胜利) |
| `const SCENE_AC` | 每场景的 AudioContext 调色(LP cutoff/IR 选择) |
| `class BootScene` | 资源预载 |
| `class TitleScene` | 标题 + 章节选择 |
| `class BattleScene` | 战斗主循环(下节展开) |
| `class HudOverlay` | HP/弹药/分数/EISEN 电报 |
| `const AudioFX = {...}` | WebAudio 合成器集合(下节) |

## 关键数据结构

- **SCENES**: `lastCapeDawn` / `blackCoveFlares` / `sandbagTrenchDusk` / `ironSeawallFog` / `cathedralRuinsVigil`
- **CHAPTERS**: 10 项数组,`{level, name, sub, scene, epigraph, boss?, pre_cutscene?}`
- **EPIGRAPHS**: 章首引言,黑屏 Courier 字幕 + 打字机 SFX
- **TYPES**: `runner`(HP30 spd0.05) / `brute`(HP70 spd0.03) / `tidelord`(HP180 near520) / `leviathan`(HP320 near600)
- **WEAPONS**: `rifle` 基础 / `shotgun` 散布 / `lmg` 高 RPM 低伤
- **EISEN_LINES**: `chapter_opens[10]` + `boss_entrance{tidelord, leviathan}` + `low_health[]` + `final_victory`
- **SCENE_AC**: `{lpCutoff, irKey, ambBedGain}` — 场景特化的 master 滤波 + IR 选择

## AudioFX 暴露 API

```
init()              首次用户手势后激活 AudioContext + masterLP + masterGain + IR
setScene(key)       切换 LP cutoff + ConvolverNode IR(5 个程序化 1.8s IR)
shoot(weapon)       枪声合成(噪声脉冲 + bandpass + 短包络)
reload()            机械咔哒声(短方波 + 噪声尾)
hit(type)           击中反馈
enemyDie(type)      死亡音(brute:厚 sub;tidelord/leviathan:子贝斯+formant)
bossRoar(boss)      BOSS 入场吼声(formant air-gasp)
phaseShift(boss)    相位切换 80→26Hz sub-drop + chirp + 白闪 hook
typewriter(len)     Eisen 电报字符 SFX
bellToll(n)         开场三连钟
ambBed(scene)       场景背景音床(海浪/雷/钟回响)
musicPlay(stem)     播 Lyria MP3(battle/boss/title/victory)
musicFade(ms)       淡出当前 stem
```

## BattleScene 主要方法

```
create()            布场景,装 HUD,载入 chapter 数据,播 epigraph
spawn(type, lane)   生成敌人 sprite(near/far 双图层 + scale 插值)
update(t, dt)       逐帧推进:敌移动/玩家瞄准/命中检测/HUD 同步
hitAt(x, y)         枪口命中判定 → 调 onHit / onKill
onKill(enemy)       加分 + AudioFX.enemyDie + 检查 boss 相位
syncHUD()           推 HP/ammo/score/wave 到 HudOverlay
showEpigraph(text)  黑屏 Courier 字幕 + typewriter SFX
showEisenLine(key)  右上角 Eisen 电报浮现
triggerBossPhase(n) HP 阈值触发:summon runners + 屏震 + roar + edgePulse
endChapter(win)     胜负判定 → 切场景或回 Title
```

## Asset pipeline

| 资产 | 工具 | 流程 |
|---|---|---|
| 场景背景 / 敌人 / Eisen 头像 | GPT-Image-2(APImart) | 4K 出图 → `scripts/chroma_key.py`(PIL 抠绿+羽化) → 缩略 |
| BOSS 8 帧 sheet | GPT-Image-2 `--image-urls` 锁身份 | 8×360px 子帧 → `scripts/build_sheet.py` 拼图 |
| 配乐 4 stems | Gemini Lyria `lyria-3-clip-preview` | curl REST → MP3 → `assets/music/` |
| 开场 / BOSS 过场 | Pippit-tool-cli `Seedance_2.0_mini` | `cut-boss5.mp4` / `cut-boss10.mp4` |

## 调参锚点

```
TYPES.tidelord.hp        180   // BOSS5 难度
TYPES.leviathan.hp       320   // BOSS10 难度
TYPES.*.speed                  // 敌移动(0.018~0.05)
TYPES.*.near_height_px         // 近景缩放上限
WEAPONS.rifle.damage           // 手感基线
WEAPONS.*.recoil / spread      // 后坐 + 散布
SCENE_AC[*].lpCutoff           // 场景闷/亮(低=闷)
PHASE thresholds 0.66 / 0.33   // BOSS 相位切换 HP 百分比
edgePulse alpha / duration     // 受击/相位红边强度
```

## Deploy

GitHub `main` → Vercel auto-redeploy(`vercel.json` 静态站点配置)。无需环境变量,纯静态。本地改 → `git push` → 等 ~30s 即生效。

## 约定

- **单文件保持**:所有游戏逻辑留在 `index.html`,不拆模块、不上构建。`index-pixel-backup.html` 是历史版本,勿动。
- **Playwright 验证**:任何 BOSS / 平衡 / 视效改动后,跑 `scripts/verify-*.mjs` 截图确认才算完成。
- **impeccable 闸门**:UI / 视觉改动前后过一遍 `impeccable` skill 标准(对比度/层级/克制)。
- **memory gate**:涉及世界观 / Eisen 台词 / no_go_themes 改动前先 `gei:memorize retrieve`,写定后 `observe → write`。
- **no_go_themes**:绝不出现 Union Jack / 任何真实国旗 / 任何 WW2 真实军事符号。世界观锁定为虚构百年诅咒。

---

## Iteration Status · COMPLETE r60

BLACKTIDE · Cycle 9 完整迭代周期(r1-r60 + r27.5/r27.6/r51.5 三个 hotfix)于 2026-06-22 收官。
- 用户指令 r58→r60 endgame 三轮后停止迭代。
- Live: <https://normandy-bunker-shooter.vercel.app>
- Repo: <https://github.com/lukeliu95/blacktide-siege-of-the-last-cape>
- 累计 64 行 ledger / 9 achievements / 4 weapons 各 3 级 / 9 codex / 5 scenes / 2 BOSS / 60 轮 AI 协作 evolution
- 后续如需重启,从 ledger r60 续 r61。
