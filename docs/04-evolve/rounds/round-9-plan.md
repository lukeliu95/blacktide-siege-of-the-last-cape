# Round 9 · 丰富游戏:多武器 + 多怪物 + 多场景(会议文案)
> 2026-06-20 · Alan 主持 · 多 sub Agent 并行资产 + 前台系统框架

## 一、需求
用户:添加更多武器选择 / 更多怪物 / 更多场景转换。

## 二、设计(第一性 + 可玩性)
### 武器系统(4 把 · 数字键 1-4 / 滚轮切换)
| 武器 | 手感 | 关键参数 |
|---|---|---|
| 重机枪 MG-42(已有) | 持续压制 | 80ms 连发 · 单发 · clip 180 |
| 霰弹枪 | 近距清场 | 7 弹丸扇形 · 慢 550ms · clip 8 · 一枪多杀 |
| 狙击步枪 | 精准爆头 | 单发高伤 5 · 700ms · clip 10 · 爆头 3× |
| 火焰喷射器 | 范围灼烧 | 锥形连续 · 低单伤高频 · 燃料 300 · 灼烧 DOT |
- 每把独立弹药(切换保留)· 独立 SFX(霰弹轰 / 步枪脆 / 火焰呼) · 独立枪口/后坐 · HUD 武器名
- 武器 POV 前景贴图:子 agent 生成(缺则回退 MG 贴图)

### 怪物扩充(4→7)
| 新怪 | 行为 |
|---|---|
| 自爆兵 Exploder | 臃肿快速,逼近碉堡自爆(大伤 + 爆炸粒子 + 震屏) |
| 投掷兵 Spitter | 中距(p≈0.6)停下,抛物线向碉堡投掷物,远程扣血 |
| 装甲军官 Armored | 正面高血(需更多弹),体型大,推进慢 |
- 新怪贴图:子 agent 生成(缺则用现有贴图染色回退)· 行为 hook 进 update()

### 场景转换(每 3 波切换)
| 场景 | 背景 |
|---|---|
| 诺曼底滩头·黎明(已有) | bg-beach |
| 夜袭·照明弹 | bg-night(子 agent 生成 4K) |
| 海堤·浓雾 | bg-seawall(子 agent 生成 4K) |
- 切换 = 淡出→换 bg→场景名 banner→淡入;场景循环

## 三、并行编排(避免 index.html 冲突:资产 agent 只产文件)
| Track | 负责 | 产出 |
|---|---|---|
| T1 新怪物贴图 | sub Agent A | assets/zombie-{exploder,spitter,armored}.png(透明) |
| T2 新武器 POV | sub Agent B | assets/gun-{shotgun,rifle,flamer}.png(透明) |
| T3 新场景背景 | sub Agent C | assets/bg-{night,seawall}.png(4K) |
| T4 武器系统 | Alan 前台 | WEAPONS 注册表 + 切换 + 多 SFX + HUD |
| T5 怪物行为 | Alan 前台 | TYPES 扩充 + explode/ranged/armored 行为 hook |
| T6 场景管理器 | Alan 前台 | SCENES + 每 3 波淡入淡出切换 + banner |
| T7 集成 | Alan | 资产到位即接,缺则降级回退 |

## 四、验收
- 1-4 切武器,手感/SFX/弹药/HUD 各异;霰弹一枪多杀、狙击爆头、火焰范围灼烧。
- 7 种怪物,自爆/投掷/装甲行为生效。
- 每 3 波场景切换,有过场 banner。
- Playwright 实测,控制台仅 favicon。资产缺失时优雅降级不报错。
