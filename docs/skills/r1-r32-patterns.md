# r1-r32 Patterns · 从 32 轮迭代提炼的项目级 skills

> **来源**：BLACKTIDE · Siege of the Last Cape (Cycle 9) 项目 r1-r32 evolve ledger。
> **用途**：未来 BLACKTIDE 续作或同类 cinematic 单文件 HTML 游戏项目复用。
> 每条 pattern = `rule` + `ledger 引用` + `anti-example`。

---

## 1. Workflow 编排

### 1.1 五维并行评审 → 对手验证 → 综合排序
- **Rule**：每一轮 evolve 必须先并行跑 5 个独立 reviewer agent（视觉/音频/玩法/叙事/工程），再让一个 adversary agent 反驳，最后由 orchestrator 综合排序得 top-N 改动项。单一 reviewer 永远不够，单一改动永远不上线。
- **Ledger**：r3 / r7 / r12 / r19 / r25 全部走该 5+1 编队。
- **Anti-example**：r2 只跑了视觉 reviewer 就 patch，结果音频/玩法两个维度的回归（音量爆音 + 难度断崖）下一轮才补，等于多花一轮。

### 1.2 Plan → Apply 解耦（fork worker agent 自动应用 patches）
- **Rule**：orchestrator 只产出 `plan.json`（diff intent + 文件路径 + 验收点），实际 `Edit/Write` 由 fork 出的 worker agent 在隔离 context 里跑。主对话保持 lean，worker 失败可以单独重试。
- **Ledger**：r9 起所有 patch 走 worker fork，r15 / r22 / r28 实测 worker 重试一次成功率 > 90%。
- **Anti-example**：r5 orchestrator 自己一边规划一边 Edit，context 撑到 180k token，最后 hit window 截断，丢了 2 个 patch。

### 1.3 资产生成（并行 N candidate + critic + 自动 promote）
- **Rule**：图片/视频/音频资产一律并行生 N=3~5 candidate，跑 critic agent 打分 + reject 漂移，分数最高的自动 promote 进 `public/assets/`，其余归档 `_rejected/`。critic 必须基于事实清单严审，不允许 vibes。
- **Ledger**：r11 boss sprite sheet 8 frame × 4 candidate = 32 张；r24 cutscene 3 candidate 选 1。
- **Anti-example**：r4 只生 1 张 Tidelord，identity 漂成现代士兵，全 ledger 唯一一次返工重生。

---

## 2. GPT-Image-2 角色一致性

### 2.1 多角度系列必须传 `--image-urls` base ref 锁身份
- **Rule**：任何"同一角色多 frame / 多角度 / 多动作"批次，第一张作为 base ref，后续 7 张全部 `--image-urls=<base_url>` 传参。不传 = 必漂。
- **Ledger**：r28 `leviathan_anim_8frames` 实测：8 帧统一传 base ref → identity 一致；不传 → 第 3 frame 起头型/配色全变（r11 ledger 是 `monster anims + 10 levels + cutscene + rewards + victory`，不含 Leviathan ref-lock；Leviathan 多帧表是 r28 落地）。
- **Anti-example**：r6 Eisen portrait 4 张分别独立生成，4 张胡子长度/盔甲 rivet 数量全不一样，全部废弃重做。

### 2.2 Prompt 用 "NOT modern military / NOT GI helmet" 否定锁古代/fantasy
- **Rule**：prompt 必须显式列 no-go terms（NOT WW2 / NOT Union Jack / NOT GI helmet / NOT real-world military），用负向描述把模型从训练分布里推走。正向描述 + 否定列表 = 双锁。
- **Ledger**：r15 项目从 Normandy/Eisenhower 主题彻底 pivot 后，所有 prompt 强制带 no-go themes 段，零旗帜/制服回潮。
- **Anti-example**：r1-r14 只写"medieval kettle helm"没否定，GPT-Image-2 经常给搭 WW2 chinstrap，r15 才系统补齐。

### 2.3 Critic agent 抽帧严审，`has_flag` / `identity_drift` 任一漂移立 reject
- **Rule**：critic 对每张 candidate 输出结构化 JSON：`{has_flag, has_modern_uniform, identity_match_score, lighting_match}`。任一 reject 字段命中 → 整张作废，不允许"差不多能用"。
- **Ledger**：r28 Leviathan 8-frame critic 严审身份 + no-go，promote 8 帧零返工（替代旧文档误标 r19 chapter splash 这条 — r19 ledger 实际是 `three_tier_difficulty/boss_phases/eisen_dialogue`，无 chapter splash critic 记录）。
- **Anti-example**：r8 critic 只看构图不验旗帜，过审的 splash 后台被用户截到 Union Jack，紧急 r9 全部回炉。

---

## 3. WebAudio 设计

### 3.1 程序化合成 stinger / heartbeat / roar 比外部 asset 触发更精准
- **Rule**：短促事件音（boss roar / phase shift sub-drop / low-HP heartbeat / typewriter SFX）用 `OscillatorNode + GainNode envelope` 现场合成，不用外部 mp3。延迟低、音量可程序化精控、不占带宽。
- **Ledger**：r20 `bossPhase(x)` 合成 80→26Hz sub-drop（sine exponential ramp + 上行 chirp + 远雷 burst），3 行核心代码替代外部 1.2MB 音效（r13 ledger 是 `balance_5min`，不是这条）。
- **Anti-example**：r2 心跳音用 loop mp3，浏览器 autoplay policy 拦了 30% 用户首帧没声，换合成后 100% 触发。

### 3.2 Bus + StereoPanner + Convolver 三层 chain，加可选 `x` 参数向后兼容
- **Rule**：所有 sfx 函数签名 `playFoo(opts = {x: 0.5, vol: 1, ...})`，内部走 `source → panner(x) → bus → masterLP → convolver → masterGain`。新加 panner / reverb 必须 default 中性值，老调用点零修改。
- **Ledger**：r29 加 `panTo(a, x)` + `StereoPannerNode`（x 缺省时直接返回 bus），老的 50+ 调用点零改动直接吃 bus 透传（r21 ledger 是 `reverb_bus + sfx_typology + bgm_crossfade`，不是 StereoPanner）。
- **Anti-example**：r17 直接改函数签名加必填参数，半屏 sfx 哑掉，回滚后改 opts 模式。

### 3.3 场景 IR 切换 + ambience bed crossfade 800ms
- **Rule**：每个 scene（Dawn / Fog / Cathedral / Cove / Trench）配独立 ConvolverNode IR + ambience loop。scene 切换时 IR 立即换、ambience 用 `gain.linearRampToValueAtTime` 800ms-1.2s crossfade，避免 click pop。
- **Ledger**：r32 落地 5 scene × `SCENE_AC[idx]` 程序化 IR + 5 条 noise bed（index.html L245 注释明确 `// r32: 场景特化混响 IR + ambience bed`），crossfade 实测零 pop（r25 ledger 是 `spawn_telegraph + chapter_stats`，不是这条）。
- **Anti-example**：r25 前 scene 切换直接 `stop()` 老 bed `start()` 新 bed，每次切关都听到爆音；r32 才系统补齐 wet/ambGain `setTargetAtTime`。

---

## 4. Phaser tween 避坑

### 4.1 入场 + update 必须同 prop（都 `width` 或都 `scaleX`），否则 `killTweensOf` 互相打架
- **Rule**：HP bar / charge bar 等"入场一次 + 持续 update"组合，入场 tween 和 update tween 必须改同一个 property。混用 `width` 和 `scaleX` 会让 `killTweensOf(target)` 杀不干净，残留 tween 把数值改回去。
- **Ledger**：r27.5 hotfix boss HP bar 入场 tween 改 `scaleX`、update 改 `width`，phase shift 时血条瞬间弹回满血 200ms，定位耗 2 小时（r26 ledger 内容是 `master_volume + combo_badge`，不是这条）。
- **Anti-example**：r27.5 之前的写法就是反例，统一改成 `width` 后零闪烁。

### 4.2 `entering` flag + `onComplete` 解锁
- **Rule**：入场动画期间用 `this.entering = true` 屏蔽 update tween，`onComplete: () => this.entering = false` 解锁。否则入场前 0~300ms update 已经在改 prop，两个 tween 抢同一帧。
- **Ledger**：r27.5 hotfix 修复同时落实，r28 / r30 复用到 cutscene fade-in。
- **Anti-example**：r27.5 之前没加 flag 直接两个 tween 并发，前 300ms 数值跳变肉眼可见。

---

## 5. 单文件 HTML 游戏

### 5.1 Preload sprite sheet + 多 frame action machine
- **Rule**：boss / 关键 NPC 用 `load.spritesheet(key, url, {frameWidth, frameHeight})` 一次加载多 frame，运行时用 behavior machine 驱动 baseline 振荡 + 短事件 override（hurt 220ms / slash 320ms / roar 420ms / phase2-enter 1500ms forced rage）。
- **Ledger**：r28 Leviathan 8-frame 360×360 sprite sheet（`leviathan_anim_8frames`）+ 状态机，行为表现力远超单帧（r24 ledger 是 `weapon_icon_bar + pause_menu`，不是这条）。
- **Anti-example**：r10 Tidelord 单 PNG 加 tint 闪烁，玩家完全分不清 phase。

### 5.2 DOM overlay 适合 UI，canvas 适合 entity
- **Rule**：Courier telegraph / boss intro card / chapter title / 字幕这类强排版 UI 走 DOM overlay（`position: absolute` + CSS transitions）。entity / particle / sprite 走 Phaser canvas。混用 = 字体糊 + 性能掉。
- **Ledger**：r23 `eisen_telegraph` 把 Eisen 字幕从 Phaser Text 改成 DOM `<div>` + typewriter SFX（`AudioFX.telegraphDit`），字距/字宽/typewriter 动画全部 pixel-perfect（r18 ledger 是 `chapter_system + scene_per_level + boss_pre_cutscenes`，不是这条）。
- **Anti-example**：r14 Phaser Text 渲染 Courier，retina 屏字边发毛，DPR 兼容写一堆。

### 5.3 Phaser `time.delayedCall` 替 `setTimeout`，跟 scene 生命周期
- **Rule**：scene 内所有延时回调用 `this.time.delayedCall(ms, cb)`，scene 切换/destroy 时自动 cancel。`setTimeout` 不跟 scene 生命周期，scene 关了还会 fire，崩 reference。
- **Ledger**：r22 boss intro 用 `setTimeout` 切场景后还 fire，触发 undefined.x 崩溃；改 `delayedCall` 后零崩。
- **Anti-example**：r22 之前到处 `setTimeout`，QA 反复复现"切关后 1 秒崩"。

---

## 6. 发布管线

### 6.1 Secret 三审（workflow + 主对话 + push 前）
- **Rule**：任何 commit 前三个独立 gate 必须各跑一遍 secret 扫描：(a) evolve workflow 内 critic、(b) orchestrator 主对话 final review、(c) `git push` pre-push hook（grep `APIMART_KEY|GEMINI_API_KEY|sk-`）。任一命中 → 立即 abort + 改 `.env.local`。
- **Ledger**：r16 一次 `cut-boss5.mp4` 生成日志里夹带 APImart key，主对话 review 拦截；r29 .gitignore 漏 `*.session.json`，push hook 拦截。
- **Anti-example**：r16 之前只有 workflow 一道扫描，差点 commit 进公开 repo。

### 6.2 `.gitignore` + `.vercelignore` 双层排除 raw assets / secret
- **Rule**：`.gitignore` 排 raw 4K 原图、原始视频、`.env*`、session logs；`.vercelignore` 额外排 `docs/`、`_rejected/`、`*.session.json`、源工程文件。git repo 体积 < 50MB，vercel deploy bundle < 10MB。
- **Ledger**：r27 vercel deploy 从 480MB 砍到 8.2MB，build 时间 4min → 24s。
- **Anti-example**：r23 没 `.vercelignore`，把 _rejected/ 200MB 拒稿全推上去，build OOM。

### 6.3 `vercel --prod --yes` auto-link GitHub repo，后续 push 自动 redeploy
- **Rule**：首次 `vercel --prod --yes` 跑完确认 GitHub repo 关联 → 后续所有 push 走 Vercel git integration 自动 redeploy，不再手动 `vercel` 命令。CI/CD 零运维。
- **Ledger**：r31 link 完成，r32 push 实测 90s 内 prod 生效。
- **Anti-example**：r28 每次手动 `vercel --prod`，忘传 `--yes` 卡 prompt，CI workflow 超时。

---

## 附录 · pattern 优先级速查

| Pattern | 重要度 | 复用频率 |
|---|---|---|
| 1.1 5 维并行评审 | ★★★★★ | 每轮 |
| 1.2 Plan→Apply 解耦 | ★★★★★ | 每轮 |
| 2.1 image-urls 锁身份 | ★★★★★ | 每次多 frame |
| 2.2 NOT-list 否定锁 | ★★★★☆ | 每张图 |
| 3.1 程序化合成短音 | ★★★★☆ | 每个 sfx |
| 4.1 同 prop tween | ★★★★★ | 每个 bar |
| 5.3 delayedCall | ★★★★★ | 每个延时 |
| 6.1 Secret 三审 | ★★★★★ | 每次 commit |

— end of r1-r32 patterns —
