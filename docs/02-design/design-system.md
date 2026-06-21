# Design System · BLACKTIDE

> **BLACKTIDE · Siege of the Last Cape — Cycle 9**
> Cinematic 2D first-person fixed-position FPS. Marshal Eisen holds the Last Cape lighthouse against the drowned dead.
> 视觉/听觉/动效语言全部围绕一个核心母题:**钟声 · 黑潮 · 一面墙**.

---

## 1. 字体层级 Typography

| 层级 | 字体 | 用法 | 例 |
|---|---|---|---|
| **Display** | `Black Ops One` (Google Fonts, 军用喷涂衬线) | 章节标题 / BOSS NAMEPLATE / WAVE 数字 / GAME OVER | `V · THE TIDELORD WAKES` |
| **Mono / Telegraph** | `Courier` (system mono fallback `Courier New`) | Eisen 电报体 `INCOMING · MARSHAL EISEN · CYCLE 9` / 调试 HUD / 弹药计数 | `Hold the toll.` |
| **Body** | `Oswald` (压扁无衬线) | 副标题 / 章节引言 epigraph / 武器名 / 提示文字 | `Hour nine. The sea is louder than my rifle.` |

**规则**:
- Display 字号 ≥ 42px,字距 `letter-spacing: 0.08em`,默认 `text-shadow: 0 0 12px var(--blood)`
- Mono 字号 14-18px,行高 1.6,Eisen 电报固定打字机 SFX + 红色脉冲边框 `--blood`
- Body 字号 16-22px,大写章节副题用 `text-transform: uppercase` + 字距 0.12em

---

## 2. 色板 Color Tokens

### 全局
| Token | Hex | 语义 |
|---|---|---|
| `--gold` | `#d8b15a` | 钟铜 / 弹壳 / HUD 主色 / 胜利 |
| `--blood` | `#c23a3a` | Eisen 电报 / BOSS 名牌 / critical HP / hit edge pulse |
| `--ink` | `#0b0d10` | 背景底层 / 字幕黑边 / vignette 核心 |
| `--bone` | `#e6dcc2` | 正文字 / 弹药数字 / 章节引言 |
| `--rust` | `#7a3a26` | 沙袋 / 铁锈 / 次要 UI 描边 |

### 5 场景 Tint(Phaser cameraColorMatrix)
| Scene | Tint Hex | 氛围 |
|---|---|---|
| **Last Cape Dawn** | `#c89a6a` | 暖橙黄,海面反光 |
| **Black Cove Flares** | `#5a7a8a` 基底 + `#ff6a3a` 闪烁脉冲 | 冷蓝 + 信号弹橙 |
| **Sandbag Trench Dusk** | `#6a5a4a` | 泥土 muddy umber |
| **Iron Seawall Fog** | `#3a4a52` | 冷灰青 + 浓雾 alpha 0.35 |
| **Cathedral Ruins Vigil** | `#2a2a3a` + `#8a6a3a` 烛光点 | 紫蓝夜 + 暖烛光 |

### BOSS 血条 3-tier 渐变
- **HP 100% → 67%**: `#d8b15a` (gold) — PHASE 1 平稳
- **HP 67% → 34%**: `#e0742a` (orange) — PHASE 2,触发增援
- **HP 33% → 0%**: `#c23a3a` (blood) + 闪烁动画 0.8s — PHASE 3 临死狂暴

---

## 3. HUD 系统

固定屏幕坐标,Phaser `setScrollFactor(0)` 锁定,所有元素带 `--blood` 或 `--gold` 1px 描边:

| 元素 | 位置 | 字体 | 颜色 | 行为 |
|---|---|---|---|---|
| **SCORE** | 左上 24,24 | Display 28px | gold | 数字滚动 200ms 缓动 |
| **WAVE** | 中上 center,18 | Display 32px | gold | 章节切换时 700ms 缩放 1.2→1.0 |
| **COMBO badge** | SCORE 下方 | Mono 16px + 圆环 | blood | 击杀刷新衰减环,4s 内未补刀消失 |
| **WEAPON icon** | 右下 -90,-80 | 256×96 sprite | tinted gold | 切枪 200ms 横向滑入 |
| **AMMO bar** | WEAPON 下方 | 分段矩形 | gold→rust | 每发减一格,reload 时整条扫光 |
| **BUNKER HP** | 底部 center | 4px 高粗条 | gold→blood (按 tier) | < 25% 触发心跳脉冲(r27 critical-HP alarm 阈值) |
| **EISEN telegram** | 上方居中浮层 | Courier 18px,黑底 + blood 描边 | bone on ink | 章节开场 / BOSS 入场 / 低血;打字机 SFX 逐字显;portrait 头像方框 84×84(r30 落地尺寸)在左,BOSS phase shift 闪红 |

---

## 4. 场景系统 SCENE_AC

5 个场景各自一套**美术差异 + camera tint + 声学预设**.声学走 `WebAudio ConvolverNode` 5 套程序化 IR:

| Scene | 美术核心 | Camera Tint | Reverb IR | Ambience Bed |
|---|---|---|---|---|
| Last Cape Dawn (L1/L2/L9) | 灯塔轮廓 + 海平线 + 沙滩占位 | `0xc89a6a` mult | 短反射 0.6s,海岸开放 | 海浪 + 海鸥 + 远钟 |
| Black Cove Flares (L3/L7) | 黑岩礁 + 信号弹弧光 + 雷雨闪 | `0x5a7a8a` + 闪光帧 | 中反射 1.2s,峡湾湿润 | 风暴雨 + 远雷 |
| Sandbag Trench Dusk (L4) | 沙袋墙堆叠 + 泥水反光 | `0x6a5a4a` mult | 极短 0.3s,泥土吞噬 | 泥泞脚步 + 低风 |
| Iron Seawall Fog (L5/L8) | 铁桩 + 雾墙 alpha 0.35 + 海堤 | `0x3a4a52` mult | 长 2.4s,金属共振 | 浓雾低鸣 + Tidelord 远吼 |
| Cathedral Ruins Vigil (L6/L10) | 断柱 + 玫瑰窗残骸 + 烛光 | `0x2a2a3a` + 烛点 | 极长 3.2s,石室教堂 | 风入残窗 + 钟摆 |

---

## 5. 动效语言 Motion Grammar

- **COMBO 衰减环**: SVG 圆环 `stroke-dashoffset` 从 0 → 满,4 秒线性,补刀重置;到点 fade 200ms.
- **Critical-HP 心跳**: BUNKER HP < 25% 时全屏 vignette `--blood` alpha 0.0 ↔ 0.35,周期 850ms,缓动 sine(r27 ledger 阈值,与代码同源).
- **BOSS phase 闪**: 触发瞬间白闪 1 帧 alpha 1.0 → 0.0 (180ms) + 屏幕 shake `intensity 0.012` 400ms + radial shockwave 圆环外扩 600ms.
- **Spawn 涟漪**: 敌人浮出时地面 1-2-3 圈水波,SVG `r` 0→80,opacity 0.7→0,800ms;Tidelord/Leviathan 出场 3 圈,半径 200.
- **弹道 tracer**: Phaser Graphics 直线 `lineStyle(2, --gold, 1.0)`,生命 60ms,fade 末段,枪口处 `addGlow` blur 12 color blood.
- **Eisen 电报浮入**: 上方滑入 280ms ease-out + 打字机 18ms/字符,字符出时 Courier 闪绿 1 帧再回 bone.
- **章节切换**: 黑场 600ms + Display 标题缩放 1.2→1.0 + epigraph Oswald 800ms fade-in.

---

## 6. 视觉资产管线 Visual Pipeline

```
GPT-Image-2 (APImart, 4K 16:9 photoreal still)
        ↓ identity prompt + --image-urls 参考锁定
        ↓ Eisen kettle-helm lion-rivet · Leviathan Cthulhu-head 8-frame
chroma_key.py  (PIL + numpy)
        ↓ HSV 容差 8-12,绿幕 / 海平面除色
        ↓ alpha-feather radius 3,边缘羽化防锯齿
resize_crop.py
        ↓ near_height_px (runner 220 / Tidelord 520 / Leviathan 600)
        ↓ 8-frame sprite sheet 360×360 per cell (Leviathan)
        ↓ idle / idle_b / roar / slash_L / slash_R / charge / hurt / phase2_rage
game-ready PNG → assets/textures/ → Phaser preload
```

**身份锁**: 主角与 BOSS 8 帧均通过 `--image-urls` 引用首帧基准图,跨帧一致性 ≥ 95%,严禁出现真实世界军服 / 国旗 / 二战意象.

---

## 7. 音频系统 Audio Stack

### WebAudio 总线
```
AudioContext
  ├─ masterGain (主音量)
  └─ masterLP  BiquadFilter lowpass (受伤/BOSS phase 衰减高频,cutoff 800Hz)
        └─ ConvolverNode  (5 套程序化 IR,场景切换时 fade 300ms)
              ├─ SFX bus     (枪声 / 击中 / 装填 / 涟漪 / 心跳)
              ├─ Voice bus   (Eisen 打字机 + 电报 ping)
              └─ Ambience bus (场景床声,loop)
```

### Lyria BGM
- 提供方: **Gemini `lyria-3-clip-preview`** 通过 curl REST 拉取 4 条管弦乐 MP3 stems:
  - `battle-theme.mp3` — L1-L4/L7-L9 普通战斗
  - `boss-theme.mp3` — L5 Tidelord + L10 Leviathan
  - `title-theme.mp3` — 主菜单 + 章节序幕
  - `victory-theme.mp3` — Cycle 9 holds 终幕
- 切歌交叉淡入 1.2s,BOSS 入场强切 + 1 拍延迟回归.

### 场景感知混响 Scene-Aware Reverb
SCENE_AC 表内每个场景一套 IR(见 §4),进场时 `convolver.buffer` 切换 + 300ms cross-fade.

### Ambience Bed
每场景一条立体声循环床声,音量 -18 LUFS,被 BUNKER HP 心跳节奏调制.

### Stereo Panning
敌人按屏幕 X 坐标做 `StereoPannerNode` 实时 panning (-0.8 → +0.8);BOSS 始终居中 0.0.

### Stinger 短促音效
- BOSS phase shift: 80→26Hz sub-drop sawtooth + 上行 chirp,400ms
- Eisen telegram: 单次 1200Hz ping + 打字机 random click
- 装填完成: 金属卡扣 + reverb tail
- combo break: 鼓边 rim shot + low pass swoop

---

## 8. 视频管线 Cutscene Pipeline

- **提供方**: `pippit-tool-cli` 调 **Seedance 2.0 mini** 生成 1080p MP4,提示词锁定 BLACKTIDE 世界观 + Eisen / Tidelord / Leviathan 形象.
- **过场清单**:
  - `cut-intro.mp4` — Cycle 9 序幕,钟塔三响
  - `cut-boss5.mp4` — Tidelord 出场前
  - `cut-boss10.mp4` — Leviathan 浪潮升起
  - `cut-victory.mp4` — Cycle 9 holds
- **回放路径 A · 直接 MP4 过场**: 全屏 `<video autoplay>` + skip 按钮(`SPACE`),播完回 Phaser scene.
- **回放路径 B · ffmpeg 抽帧透明叠加**:
  ```
  ffmpeg -i cut.mp4 -vf "fps=24,chromakey=0x000000:0.1:0.2" -c:v png frame_%04d.png
  ```
  → 透明 PNG 序列叠在 Phaser 场景上层,做"幽灵 Leviathan 触手从屏外伸入"等局部动画,SCREEN blend mode 与 WebGL 主场景合成.

---

**总纲**: 一切视觉/听觉/动效服务于 **"一人 · 一墙 · 百年"** 的孤独压迫感.金色 = 希望未灭,血红 = 黑潮未退,墨黑 = 钟楼第三响之后的死寂.
