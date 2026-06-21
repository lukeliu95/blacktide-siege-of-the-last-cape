# Evaluation Framework · 诺曼底碉堡

## 评估维度
| 维度 | 指标 | 阈值 | 方法 |
|---|---|---|---|
| 可启动性 | 标题屏渲染、无致命报错 | PASS | Playwright 导航 + console error 检查 |
| 核心循环 | 开始→敌人涌出→射击命中→计分→碉堡掉血→GameOver | 全链路 PASS | 脚本注入操作 + 状态断言 |
| 射击手感 | 子弹/火光/弹壳/血花/震动存在 | 主观 PASS | 截图 + 代码核查 |
| 波次推进 | 波次数量/速度/血量随 wave 递增 | PASS | 读 `startWave()` 参数 |
| 平衡 | 单波可在弹药约束下守住 | 主观可玩 | 实测击杀/掉血比 |
| 设计质量 | 字体层级 / 对比 / 像素一致性 | impeccable PASS | impeccable 闸门 |
| 持久化 | best 写入 localStorage | PASS | 代码核查 |
| 可访问性 | 触屏可玩、提示清晰 | PASS | touch 事件核查 |

## 测试用例(关键)
- TC-1 启动:导航即出标题,error 仅 favicon 404 → PASS
- TC-2 开始:点击 → `state==='play'`,`enemies` 开始生成 → PASS
- TC-3 命中计分:对准敌人连续开火 → `score`/`killCount` 增长 → PASS(实测 30 分/3 杀)
- TC-4 碉堡掉血:敌人逼近 → `bunkerHP` 下降(实测 100→97)→ PASS
- TC-5 设计闸门:impeccable 扫描 → No anti-patterns → PASS
