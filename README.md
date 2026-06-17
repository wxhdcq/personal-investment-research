# Personal Investment Research

`personal-investment-research` 是一个中文个人投资研究 Codex Skill，用于辅助长期投资、股票和 ETF 分析、仓位规划、持仓复盘、估值分析和风控。它的目标不是喊单，而是帮助用户把投资判断拆成事实、数据来源、市场预期、个人推断、执行方案和判断失效条件。

## 用途

适合用于：

- 分析美股、ETF、半导体、DRAM、AI、云计算、黄金、现金和短债等资产。
- 规划核心仓、趋势仓、防御仓和现金仓。
- 回答“现在能不能买”“还能不能加仓”“该不该减仓”“ETF vs 个股”“二选一”等问题。
- 做持仓复盘、财报复盘、估值分析、止盈止损和交易计划。
- 在缺少实时数据时，改用条件式分析并明确说明数据缺失。

不适合用于：

- 简单金融概念定义，例如“什么是 meme 股”。
- 纯财经文本翻译。
- 泛泛的金融教育，不涉及具体标的、组合或执行问题。
- 保证收益、稳赚不赔、内幕交易、操纵市场、规避监管或短线暴富请求。
- 替用户做最终投资决定或接入真实券商自动下单。

## 安装

将整个目录复制到以下任一位置：

```text
~/.agents/skills/personal-investment-research
```

或项目内：

```text
.agents/skills/personal-investment-research
```

如果你的 Codex 环境使用其他技能目录，例如 `~/.codex/skills` 或 `$CODEX_HOME/skills`，请放到对应的 skills 目录下，并保持目录名为 `personal-investment-research`。

## 显式调用示例

```text
使用 $personal-investment-research，分析 MU 最近上涨原因，并给出是否适合继续加仓的三套方案。
```

```text
使用 $personal-investment-research，比较 QQQM vs VOO，哪个更适合作为我的长期核心仓？
```

```text
使用 $personal-investment-research，复盘我现在的 QQQM、NVDA、META、MSFT 持仓，并给出加仓和减仓规则。
```

## 数据源规则

涉及实时股价、财报、新闻、估值、利率、汇率、ETF 持仓或公司指引时，应优先使用：

- 公司财报、10-K、10-Q、8-K、投资者关系页面。
- Earnings call transcript。
- ETF 官方页面和持仓文件。
- SEC、Nasdaq、NYSE。
- FRED、美联储、美国财政部。
- Reuters、Bloomberg、CNBC、MarketWatch、Seeking Alpha 等辅助来源。

如果当前环境无法联网或无法确认实时数据，必须明确说明“当前无法确认实时数据”，不能假装拥有最新行情。

## 风险免责声明

本 Skill 只用于个人投资研究和学习，不构成投资顾问服务，也不提供保证收益承诺。任何输出都应被视为研究框架和执行纪律建议，而不是最终投资决定。用户需要结合自己的总资金、已有持仓、投资期限、风险承受能力、币种、账户市场和税务情况独立判断。
