# Round 1 · 字体层级 + 全链路验证

## 提议(老吴视角)
首版 `index.html` 全程单一等宽字体,impeccable 设计闸门报 `single-font`(缺乏字体层级)。提议:引入像素展示字体做标题/提示,正文 HUD 保留等宽,形成层级;并用 Playwright 起 http 服务器跑全链路自测。

## 变更
1. 引入 `--font-display: "Press Start 2P"`(Google Fonts CDN,离线降级等宽)用于底部提示。
2. 正文/HUD 保留 `--font-body: "Courier New"` 等宽。
3. Playwright 验证:导航、标题屏截图、点击开始、状态断言、注入射击循环断言计分/掉血。

## 结果
- impeccable 复扫:**No anti-patterns**。
- 功能实测:`state` 正确流转;wave 1 生成 5 敌;连续命中 → score 30 / killCount 3;敌人逼近 → bunkerHP 100→97。
- 控制台:仅 favicon 404(无害)。

## CEO 裁决:KEPT
字体层级零玩法风险、提升像素街机识别度;验证证据充分。保留并交付。

## Δ
`+design_pass +verified`(质量门通过 + 全链路验证通过)
