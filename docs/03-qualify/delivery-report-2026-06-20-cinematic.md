# 交付报告 v2 · 诺曼底防线:亡兵浪潮(电影级真实感)
> 2026-06-20 · GEI Agent Studio

## 一句话
第一人称电影级真实感波次射击:守住诺曼底碉堡,用真实机枪扫射从海岸涉水扑来的真人级亡兵浪潮(普通兵/快速兵/防毒面具精英/超级壮硕兵)。

## 技术栈
- **框架**:Phaser 3.80(CDN,零构建)— 现成全功能 2D 游戏框架
- **美术**:GPT-Image-2(APImart · 4K)真人级背景 + 怪物;`chroma_key.py`(PIL+numpy)绿幕抠图
- **音效**:WebAudio 程序化
- **字体**:Black Ops One(标题)+ Oswald(HUD)

## 交付物
| 文件 | 说明 |
|---|---|
| `index.html` | Phaser 游戏主体(电影级版本) |
| `index-pixel-backup.html` | 首版像素风(已归档备份) |
| `assets/bg-beach.png` | 4K 电影感诺曼底滩头背景 |
| `assets/zombie-{soldier,runner,elite,brute}.png` | 4 种真人级僵尸(透明) |
| `assets/gun-fp.png` | 第一人称真实机枪前景(透明) |
| `assets/chroma_key.py` | 绿幕抠图脚本(可复用,加新兵种用) |
| `docs/demo/hero-cinematic.jpg` | 实测英雄镜头 |

## 怎么玩
```bash
cd /Users/lukeliu/gei-workspace/output/normandy-bunker-shooter
python3 -m http.server 4180   # http://localhost:4180/index.html
```
鼠标瞄准 · 按住左键持续开火 · R 换弹 · P 暂停。守住碉堡,撑过每一波。

## 质量结论
| 项 | 结果 |
|---|---|
| Phaser + 5 资产加载 | ✅(控制台仅 favicon 404) |
| 真人级背景 + 4 兵种 + 第一人称武器合成 | ✅ 电影质感(hero-cinematic.jpg) |
| 透视逼近(远小→近大) | ✅ scale 0.03→full,四兵种体型错落 |
| 正面火力(火光/曳光/震动/血雾) | ✅ |
| 波次/兵种差异/连杀/碉堡血量/补给/换弹/最高分 | ✅ |
| 游戏结束流程 | ✅ |
| 设计闸门 impeccable | ✅ No anti-patterns |

**判定:FINALIZE**

## 已知边界 / 递弱代偿
- 真人贴图为**单帧静像 + 程序化运动**(逼近放大/晃动/受击),非逐帧行走动画——这是 GPT 出图无法保证逐帧一致下的现实最优解,换来真人质感。
- 僵尸为虚构怪物设定(过 AI 安全审核,非血腥写实)。
- 字体 + Phaser 走 CDN,需联网;离线时字体降级、Phaser 需本地化(后续可 vendor)。

## 后续可选
更多兵种(自爆兵/投掷兵)· BOSS 浪(登陆艇巨兽)· 武器升级(霰弹/火焰)· VEO3 出动态过场 · Phaser 本地 vendor 离线化 · 移动端触屏射击。
