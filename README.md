# Personal Investment Research

`personal-investment-research` 是一个中文个人投资研究 Codex Skill，用于股票和 ETF 分析、仓位规划、持仓复盘、买入/卖出计划、估值和财报复盘、风险控制。它帮助用户建立投资判断框架，不承诺收益，也不替用户做最终投资决定。

## 用途

- 分析具体股票、ETF、黄金、现金和短债等资产。
- 做核心仓、卫星仓、趋势仓和现金仓的比例规划。
- 复盘持仓集中度、买入理由、风险暴露和下一步动作。
- 比较 ETF vs 个股，或做两只标的的二选一。
- 制定买入、加仓、减仓、止盈、止损和再平衡规则。

## 安装方式

个人级 Skill：

```bash
mkdir -p ~/.agents/skills
cp -R personal-investment-research ~/.agents/skills/
```

项目级 Skill：

```bash
mkdir -p .agents/skills
cp -R personal-investment-research .agents/skills/
```

如果你的 Codex 环境使用 `~/.codex/skills` 或 `$CODEX_HOME/skills`，也可以复制到对应 skills 目录下。目录名应保持为 `personal-investment-research`。

## 显式调用示例

```text
$personal-investment-research 分析 NVDA 现在还能不能买，并给我稳健、中性、进取三套方案。
```

```text
$personal-investment-research 比较 QQQM vs VOO，哪个更适合作为长期核心仓？
```

```text
$personal-investment-research 复盘我的持仓，并给出加仓、减仓和止盈止损规则。
```

## 适合场景

- 用户要求具体股票或 ETF 分析。
- 用户要求组合配置、仓位比例或持仓复盘。
- 用户要求现在能不能买、还能不能加仓、是否减仓。
- 用户要求财报、估值、行业催化或风险清单。
- 用户要求明确执行方案、失效条件和复盘时间点。

## 不适合场景

- 简单金融概念定义，例如“什么是 meme 股”。
- 纯财经文本翻译。
- 泛泛金融教育，不涉及具体标的、组合或执行问题。
- 保证收益、稳赚不赔、内幕交易、操纵市场、规避监管或短线暴富请求。
- 自动下单、保存券商账号密码或接入真实券商交易。

## 数据源规则

涉及实时股价、财报、估值、ETF 持仓、利率、汇率、新闻催化、监管变化、公司指引、重大并购、诉讼、制裁或会计问题时，必须获取或要求最新数据。

数据源优先级：

1. 公司 IR、SEC、ETF 官方页面和持仓文件、交易所。
2. Reuters、Bloomberg、CNBC、WSJ、FT。
3. Yahoo Finance、MarketWatch 等辅助数据源。
4. 论坛、Reddit、X 只能作为观点或情绪参考，不能作为事实核心。

如果无法获得最新数据，必须说明数据缺口，并将结论降级为框架分析。

## 风险免责声明

本 Skill 只用于个人投资研究和学习，不是个性化投资、税务或法律建议。输出应被视为研究框架和执行纪律建议，而不是最终投资决定。用户需要结合自己的总资金、已有持仓、投资期限、风险承受能力、币种、账户市场和税务情况独立判断。

## 验证方法

```bash
python scripts/validate_skill.py
```

验证脚本会检查 `SKILL.md` front matter、`agents/openai.yaml`、`evals/prompts.csv` 和 Markdown 行长度等基础工程质量。
