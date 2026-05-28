# 学术 Skill 索引

本仓库在 `.cursor/skills/` 下提供 **26** 个 Cursor Agent Skill，按用途分为 7 类。Cursor 会从项目路径 `.cursor/skills/`（及兼容路径 `.agents/skills/`）自动发现各目录中的 `SKILL.md`。

## 编排 · orchestration（4）

端到端流水线：研究 → 写作 → 审稿。

| Skill | 说明 |
|-------|------|
| `academic-pipeline` | 全流程编排（研究、写作、完整性检查、审稿、修订） |
| `deep-research` | 13-agent 深度研究（系统综述、事实核查等） |
| `academic-paper` | 12-agent 学术论文写作流水线 |
| `academic-paper-reviewer` | 多视角模拟同行评议 |

## 研究 · research（8）

选题、文献、引用与 AMiner 检索。

| Skill | 说明 |
|-------|------|
| `research-ideation` | 5W1H、缺口分析、研究规划 |
| `literature-review` | 系统文献综述（多数据库） |
| `citation-management` | DOI/BibTeX、Scholar/PubMed 检索与校验 |
| `citation-verification` | 引用准确性核验指南 |
| `aminer-academic-search` | AMiner 全功能学术 API |
| `aminer-deep-search` | 深度多轮文献采集（ReAct） |
| `aminer-free-academic` | AMiner 免费层 API |
| `aminer-daily-paper` | 每日论文推荐 |

## 分析 · analysis（3）

实验结果与统计分析。

| Skill | 说明 |
|-------|------|
| `results-analysis` | 严格统计分析与图表解读 |
| `results-report` | 实验结果结构化报告 |
| `statistical-analysis` | 检验选择、贝叶斯、效应量 |

## 写作 · writing（5）

成稿、反 AI 痕迹与会议论文模板。

| Skill | 说明 |
|-------|------|
| `scientific-writing` | IMRaD、LaTeX 模板、报告规范 |
| `writing-anti-ai` | 去 AI 写作痕迹（中英） |
| `ml-paper-writing` | NeurIPS/ICML/ICLR 等 ML 会议论文 |
| `doc-coauthoring` | 协作文档 / RFC / 技术规格 |
| `paper-self-review` | 投稿前自检清单 |

## 审稿 · review（2）

正式评议与回复审稿人。

| Skill | 说明 |
|-------|------|
| `peer-review` | 结构化同行评议（CONSORT/STROBE 等） |
| `review-response` | Rebuttal 与审稿意见回复 |

## 办公 · office（3）

Word / PDF / PPT 处理。

| Skill | 说明 |
|-------|------|
| `docx` | Word 创建、修订、批注 |
| `pdf` | PDF 读写、合并、表单、OCR |
| `pptx` | 演示文稿编辑与生成 |

## 工具 · utilities（1）

| Skill | 说明 |
|-------|------|
| `defuddle` | 网页正文提取为 Markdown |

## 来源

| 来源 | Skills |
|------|--------|
| galaxy-dawn/claude-scholar | research-ideation, citation-verification, results-*, writing-anti-ai, paper-self-review, review-response, doc-coauthoring, ml-paper-writing |
| k-dense-ai/scientific-agent-skills | literature-review, citation-management, statistical-analysis, scientific-writing, peer-review, docx, pdf, pptx |
| canxiangcc/aminer-open-skill | aminer-*（4 个） |
| kepano/obsidian-skills | defuddle |
| 本仓库编排 | academic-paper, academic-paper-reviewer, academic-pipeline, deep-research |

## 在本机激活

项目级（打开本仓库即生效）：

```bash
# Skill 已在 .cursor/skills/ 下，无需额外步骤
```

全局（所有项目可用）：

```bash
ln -sfn "$(pwd)/.cursor/skills" ~/.cursor/skills
# 或复制：cp -a .cursor/skills ~/.cursor/skills
```

Cloud / CI 环境：

```bash
./scripts/activate-skills.sh
```
