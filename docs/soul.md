# BLACKTIDE · Soul Codex

> 这份档案是 BLACKTIDE 世界观的唯一事实源。
> 任何生成图 / 视频 / 音乐 / 文案的 agent 必须先读这份再下笔。
> **内容漂移就杀掉重做。**
>
> — Cycle 9, Last Cape

---

## I. 世界观 · The Cycle

**标题:** BLACKTIDE · Siege of the Last Cape
**当前周期:** Cycle 9
**Tagline:** A cinematic 2D first-person fixed-position FPS where Marshal Eisen holds the Last Cape lighthouse against the drowned dead of the Black Tide.

### 设定核心

每一百年,一道名为 **BLACK TIDE** 的诅咒从海底涌起,把溺亡之死者(**the drowned dead**)推上岸,扑向 **Last Cape**(最后之岬)上唯一一座灯塔要塞。这是 **Cycle 9** — 诅咒的第九次轮回。

**Marshal Eisen** 是这座灯塔的孤独守夜人(sole warden)。
一墙。一岬。一岸。
一百年的不让步。

钟楼在退潮时敲响三声(**three tolls at low tide**)。
**死者最先听见。**

### 三个不可变的母题
1. **CYCLE / 周期** — 一切已经发生过八次,Eisen 知道第五关墙会破,知道终末会迎来 Leviathan。这是宿命论的恐怖,不是好奇心驱动的探索。
2. **TIDE / 潮汐** — 战斗节奏 = 潮汐节奏。低潮 = 静默 = 钟响 = 死者醒。高潮 = 涌浪 = boss 显现。
3. **HOLD / 坚守** — 这不是进攻型游戏。玩家(=Eisen)固定不动,角色被困在阵地上。胜利的定义不是夺取,是 **"不让它过来"**。

### 时间感
不要写"分钟"或"小时"作为现代度量。用 **"hour one of Cycle 9"** / **"low tide"** / **"third toll"** / **"between the lightning"**。

---

## II. Marshal Eisen · 主角画像

> "I dreamed of you, Tidelord."
> — Eisen, Level 5 boss entrance

### 身份锁定

- **名字:** Marshal Eisen
- **角色:** Last warden of the Last Cape lighthouse
- **存在形式:** Eisen 从不作为实体出现在场景中。他**就是**玩家视角。他的声音以 Courier 字体的"电报"形式到达屏幕(`INCOMING · MARSHAL EISEN · CYCLE 9`),配打字机音效;在 boss 阶段切换时他的肖像红光闪烁。

### 外形(画肖像 / 头像 / 头盔特写时严格遵守)

- 中世纪 **kettle helm**(壶盔),铆钉处铸成 **lion-head**(狮首)纹章。
- 风霜留疤的络腮胡(scarred weather-worn beard)。
- 冷峻凝视(cold stern gaze)。
- 皮质钉甲(leather studded armor)。
- 整体气质 = **古代石头要塞的指挥官**,不是 WW2 GI,不是现代士兵,不是科幻战士。

### 性格底色

- **疲惫**(weary)但**不绝望**(not despairing)。
- 已经活过八次轮回 → **斯多葛**(stoic),不哭嚎,不豪言。
- 信念不是"我能赢",而是 **"我能守到下一次钟响"**。

### 台词原则(Voice Register)

风格名: **"Spartan field-log telegrams"**

- 写法 = 短句电报。**几乎不超过 8 个英文单词。**
- 视角混用: **第二人称命令**("Hold the toll.") + **第一人称片段**("It is louder than I remember.")。
- **绝不解释**。绝不抒情铺陈。
- **没有现代俚语,没有粗口,没有政治词汇,没有任何品牌 / 国家 / 时代标记。**

可直接引用的真台词(EISEN_LINES 已锁,**不要改写**):

```
Hold the toll.
Seawall — do not yield.
They come from the cove. Hold.
Knees in mud. Eyes up.
Tidelord. I know your shape.
In a chapel. With a rifle.
Count the lightning. Aim between.
It is louder than I remember.
Last cape. Last bell.
Leviathan. End of Cycle 9.

—— Boss 入场 ——
I dreamed of you, Tidelord.
You woke the sea. I end it.

—— Low HP ——
Bunker's bleeding.
One more wave. One more.
Not today. Not Cycle 9.

—— 终末胜利 ——
Cycle 9 holds.
```

---

## III. 反派阵营 · The Drowned

### 三类杂兵(共 7 种变体,统称 **the drowned dead**)

> 共通锁身份描述词: **"drowned-dead siege wraith, barnacle-encrusted bone armor, kelp-strung ribcage, waterlogged grey-green skin, hollow phosphorescent eyes, salt-crusted rags, sea-rot decay, NOT zombies, NOT humans, NOT WW2 soldiers"**

- **Runner / 步兵**: 冲刺型,瘦长,赤足陷泥,挥锈断刀。
- **Brute / 重甲**: 慢重,壳厚,锈铁面罩 + 海葬甲胄。
- **Caster / 远程**: 举骨号角或鲸骨长矛,从远岸吐黑气。**Caster 是代码中 `spitter` 兵种(Drowned Spitter, behavior:'ranged', 远端吐黑胆汁)的世界书皮肤。** 完整代码兵种集为 7 杂兵(`soldier` / `runner` / `elite` / `brute` / `exploder` 自爆 / `spitter` 远程 / `armored` 重甲)+ 2 boss(`tidelord` / `leviathan`),Caster 对应其中之一,其余在 Codex(`CODEX[*].lore`)中各有皮肤化身。

每个杂兵的行为机制由 wave generator 控制,但**视觉锁死在以上描述词内**,不允许出现"现代僵尸 / 病毒感染者 / 哥布林"等替换。

### Boss 1 · TIDELORD(Level 5)

- HP 180 · 单击伤 35 · 击杀分 600
- 入场速度 0.022 · 近景高 520px
- **三阶段**: 100% → 66%(PHASE 2)→ 33%(PHASE 3)。每次阶段切换召唤 2-3 runner + 屏幕震动 + bossRoar 音效 + 红色边缘脉冲。
- **音色签名**: Sub-bass 双锯齿 + formant 气音咆哮。阶段切换时 80→26Hz 次低频下坠 + chirp。
- **叙事**: 一个比这座岬更老的次级存在。每一个 Cycle 都是 Tidelord 把防线击穿。**Cycle 9 是第一个它没破线的轮回。**
- **锁身份描述词**: **"drowned-tide overlord, half-skeletal armored warlord, barnacle-plated pauldrons, kelp cape, hollow blue-flame eyes, two-handed corroded greatblade, ankle-deep in black surf, NOT a knight, NOT a demon lord, NOT humanoid pretty"**
- Eisen 入场台词: **"I dreamed of you, Tidelord."**
- 预过场: `cut-boss5.mp4`

### Boss 2 · LEVIATHAN OF THE BLACK TIDE(Level 10 终)

- HP 320 · 单击伤 45 · 击杀分 1200
- 入场速度 0.018 · 近景高 600px
- **三阶段**: 100% → 66%(PHASE 2)→ 33%(PHASE 3)。PHASE 2 触发 sub-bass 坍塌 + 白闪 + 径向冲击波 + 红 phaseVig。
- **8 帧多角度动画 sprite sheet**(每帧 360×360):
  `idle / idle_b / roar / slash_left / slash_right / charge / hurt / phase2_rage`
- **音色签名**: 高音触手咆哮变体;PHASE 2 sub-bass 崩塌。
- **叙事**: 百年周期的终末顶点。它倒下 = 岬守住。
- **锁身份描述词**(GPT-Image-2 必须使用 `--image-urls` 参考帧锁定身份,8 帧一致):
  **"Cthulhu tentacle-head sea horror, NOT humanoid skull face, NOT pretty,  black wet barnacle-encrusted heavy armor, claw hands, NO chest glow, earthy palette of black-brown-rust-deep-teal, towering siege titan, drowned colossus rising from black surf"**
- Eisen 入场台词: **"You woke the sea. I end it."**
- 预过场: `cut-boss10.mp4`

---

## IV. 视觉调性 · Visual Codex

### 色板(严格)

- **主色**: 黑潮深蓝绿(deep teal-black `#0a1418`),鲸骨灰(bone-grey `#8a8478`),铁锈红(rust `#7a2a1e`),磷火蓝(phosphor blue `#3a8aa0`)。
- **强调**: 退潮黎明的橘金(low-tide amber `#c8702a`)用于灯塔光、火炬、信号弹。
- **绝禁**: 鲜红(`#ff0000`)、电青(neon cyan)、霓虹粉、纯白主体、绿色光剑、任何 RGB 高饱和"游戏感"颜色。
- **boss 阶段切换时短促红闪**(`#a02020` 边缘 vignette)是唯一允许的高饱和红,持续 < 200ms。

### 光照

- **来源**: 灯塔光柱(`lighthouse beam`)+ 闪电(`storm flash`)+ 信号弹(`signal flare`)+ 火炬(`brazier`)。**绝无日光。**
- **方向**: 几乎都是 **back-lit / rim-light**。Eisen 看到的死者是逆光剪影 + 磷火眼孔。
- **雾**: 海雾 + 火药烟 + 焚尸黑烟,常驻 0.3-0.6 alpha。

### 构图

- **第一人称固定机位**,垂直对称,墙在前,海在后,死者从远景小→近景大压来。
- 远景层 / 中景战线 / 近景沙袋钢钉 = 三段景深,**永远三段**。
- HUD 极简: 顶部 toll/wave/score,底部 HP/ammo,中央十字准星。其余空间留给海。

### 场景常量(已锁)

| Scene Key | Visual |
|---|---|
| Last Cape Dawn | 退潮黎明,灯塔剪影,湿沙银光 |
| Black Cove Flares | 黑色海湾,信号弹橘红投影 |
| Sandbag Trench Dusk | 黄昏战壕,泥膝深,沙袋潮湿 |
| Iron Seawall Fog | 铁锈海墙,浓雾,水从墙里渗出 |
| Cathedral Ruins Vigil | 教堂废墟,断钟仍悬,蜡烛与闪电 |

---

## V. 声音调性 · Audio Codex

### 哲学
**"海比枪响。"** — Eisen, Level 8
音乐不是装饰,是潮汐的另一个声道。

### 三层声场

1. **管弦层(Lyria)**: 真乐器 MP3 stems — `battle-theme` / `boss-theme` / `title-theme` / `victory-theme`。低音弦 + 战鼓 + 远处合唱,**没有电子合成 lead,没有 epic trailer brass hit**。
2. **环境层(WebAudio + 5 IR)**: 浪、风、雾笛、远雷、海鸥(稀少)、钟尾鸣。每个场景一个特化 ConvolverNode reverb IR(1.8s)。
3. **SFX 层(WebAudio 合成)**: 枪声 = 闷重 + 低频塌陷,**不是现代步枪 crack**。boss 咆哮 = sub-bass + formant 气音。Eisen 电报 = 打字机咔哒 + 单声道低通。

### 禁声

- 没有电吉他。
- 没有 dubstep / EDM drop。
- 没有现代女声 pop vocal。
- 没有"epic cinematic BWAAAH"trailer 喇叭。
- **合唱可以,但必须是远而干涸的,像石教堂里十个老兵在低吼,不是 Hans Zimmer 60 人团。**

---

## VI. 文案调性 · Field Log Voice

### Eisen 字幕电报格式

```
INCOMING · MARSHAL EISEN · CYCLE 9
> Hold the toll.
> They come from the cove.
```

- 全大写 header,Courier 字体,打字机 SFX。
- 内文小写,`> ` 前缀,每行 ≤ 8 词。
- **不用感叹号。** 不用省略号超过一次。
- 不用 emoji。不用粗体。不用 markdown 格式符号。

### Epigraph(章首铭文)风格

每章开场一行铭文。已锁的十句:

```
I.   The bell tower tolled thrice at low tide. The dead heard it first.
II.  Hour one of Cycle 9. The seawall is wet from the inside.
III. Seven flares fired into the cove. Seven flares the cove returned.
IV.  Knee-deep in cold mud. Their hands close on my ankles before I see them.
V.   Every Cycle the line breaks here. The last marshal did not write why.
VI.  The crypt door was barred from the outside. It is no longer barred.
VII. Lightning every fifteen seconds. I have learned to aim in the dark between.
VIII.Hour nine. The sea is speaking my name in my mother's voice.
IX.  One wall. One marshal. One hundred years of held ground.
X.   Cycle 9 ends tonight. The Leviathan or me. Not both.
```

**这些不要改一个词。** 任何 epigraph 重写必须保持: 短句 + 具体细节 + 一个反转钩(seven returned / no longer barred / mother's voice)。

### 用词禁忌

- ❌ "soldier" / "army" / "battalion" → ✅ "marshal" / "warden" / "line"
- ❌ "monster" / "creature" / "enemy" → ✅ "the drowned" / "the dead" / "they"
- ❌ "level" / "stage" / "round" → ✅ "toll" / "wave" / "hour"
- ❌ "score" / "kill count" → 在叙事文本中只说 "held" / "did not yield"
- ❌ "boss fight" → ✅ "the Tidelord woke" / "the Leviathan rose"

---

## VII. 严禁元素 · Hard Negative List

> 以下短语**必须**出现在所有 GPT-Image-2 / Pippit / Lyria 的 negative prompt 中。**英文短语形式,可直接复制粘贴。**

```
NEGATIVE_PROMPT_VISUAL =
  "no Union Jack, no British flag, no American flag, no any national flag,
   no heraldry, no royal crest, no coat of arms,
   no WW2 imagery, no Normandy D-Day, no Eisenhower reference,
   no real-world soldier uniform, no Wehrmacht, no swastika, no Nazi symbol,
   no modern military vehicle, no tank, no helicopter, no jet, no humvee,
   no modern firearm brand, no AK-47 silhouette, no M16 silhouette,
   no cyberpunk neon, no synthwave grid, no anime big-eye style,
   no Disney cute, no chibi, no pixel art,
   no celebrity face, no real person likeness,
   no text overlay, no watermark, no logo, no UI mockup,
   no high-saturation RGB, no neon pink, no neon cyan,
   no daylight blue sky, no green grass field,
   no humanoid pretty face on bosses, no anime demon lord,
   no zombie virus tropes, no biohazard symbol"

NEGATIVE_PROMPT_AUDIO =
  "no electric guitar, no dubstep, no EDM drop, no synthwave lead,
   no modern pop vocal, no trailer brass BWAAAH, no Hans Zimmer 60-piece choir,
   no whistle melody, no children chorus, no ethnic flute solo"

NEGATIVE_PROMPT_TEXT =
  "no modern slang, no profanity, no political reference,
   no brand name, no country name, no real war reference,
   no exclamation mark, no emoji, no markdown bold, no all-caps shouting"
```

**漂移检测**: 任何产出若含以上任一元素,**直接退回重做**,不允许"差不多就行"。

---

## VIII. Prompt 模板 · Reference Prompts

> 以下三段是经过实战验证、已锁定在 r15 之后的参考 prompt。新内容生成时**先 fork 这些模板再改细节**,不要从零写。

### A. GPT-Image-2(Boss 立绘 / 杂兵 sprite / 场景 still)

```
A cinematic 2D first-person game still from BLACKTIDE Cycle 9.
[SUBJECT: Leviathan of the Black Tide — Cthulhu tentacle-head sea horror,
 NOT humanoid skull, black wet barnacle-encrusted heavy armor, claw hands,
 NO chest glow, towering siege titan, ankle-deep in black surf.]
Scene: Cathedral Ruins Vigil — broken stone arches, hanging bell,
 storm sky with single lightning flash rim-lighting the silhouette.
Palette: deep teal-black #0a1418, bone-grey, rust #7a2a1e, phosphor blue eyes,
 low-tide amber #c8702a on torch only.
Lighting: heavy back-lit rim, fog 0.5 alpha, no daylight, no high saturation.
Composition: vertical symmetry, fixed first-person camera, three-depth layering
 (foreground sandbags / mid-line skirmishers / far giant silhouette).
Style: matte painting, oil-on-canvas grain, no anime, no pixel, no 3D render look.

NEGATIVE: [paste NEGATIVE_PROMPT_VISUAL here]

# Identity lock — pass previous frame as reference:
--image-urls https://.../leviathan-ref-frame-01.png
```

### B. Lyria(管弦 stem 生成)

```
Genre: dark orchestral siege, fog-shrouded coastal battle, gothic chamber strings.
Instruments: low strings (cello + double bass), distant war drum,
 dry stone-chapel male choir (8-10 voices, no soloist),
 single church bell tail, no electric guitar, no synth lead.
Mood: weary stoic defiance, century-long held ground, slow tidal build.
Tempo: 72 BPM, 4/4, sub-bass swells on bar 1 and 3.
Reference: late Howard Shore Mordor + early Mick Gordon ambient cuts —
 NOT trailer BWAAAH, NOT Hans Zimmer 60-piece, NOT epic uplift.

Length: 90s loop, seamless head-tail.

NEGATIVE: [paste NEGATIVE_PROMPT_AUDIO here]
```

### C. Pippit / Seedance(过场视频 cut-bossN.mp4)

```
Cinematic 5-second pre-boss cutscene for BLACKTIDE Cycle 9.
Camera: fixed first-person ground-up POV, slow 5% dolly forward.
Subject: Leviathan rising from black surf, water cascading off barnacle armor,
 tentacle head writhing, single lightning flash rim-lights silhouette on frame 60.
Scene: Cathedral Ruins Vigil at storm dusk.
Palette + lighting + composition: see Soul Codex IV.

Audio bed: low-frequency rumble + distant chapel bell + Eisen telegram SFX
 on frame 90 with on-screen text "INCOMING · MARSHAL EISEN · CYCLE 9 /
 > You woke the sea. I end it."

NEGATIVE: [paste NEGATIVE_PROMPT_VISUAL + NEGATIVE_PROMPT_AUDIO here]

# Identity lock for Leviathan across 8 frames:
--image-urls leviathan-sheet-frame-01.png ... leviathan-sheet-frame-08.png
```

---

## IX. Drift Audit Checklist · 漂移自检清单

任何新产出落地前,**逐条打勾**:

- [ ] 没有任何真实国家 / 旗帜 / 军装 / WW2 元素
- [ ] 没有"现代僵尸""anime demon""cyberpunk""epic trailer"美学
- [ ] 配色在 Codex IV 锁定范围内
- [ ] 光照是 back-lit / rim-light,无日光
- [ ] Boss 身份锁描述词 100% 包含
- [ ] Eisen 台词 ≤ 8 词、Courier、无感叹号、无 emoji
- [ ] Epigraph 未被改写
- [ ] negative prompt 已粘贴完整三段

任何一项不过 → **杀掉重做**,不允许"差不多就行"。

---

> *Last cape. Last bell.*
> *Cycle 9 holds.*
>
> — END SOUL CODEX —
