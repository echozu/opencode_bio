---
name: prompt-optimizer
description: >
  MANDATORY at the START of every new analysis session (Phase 0, before Domain Anchoring).
  Use when a user provides an analysis request — this skill reads data paths, parses user intent,
  optimizes the prompt for clarity and completeness, and returns it to the user for confirmation
  before proceeding. Ensures analysis goals, data types, and parameters are explicitly defined.
---

# Prompt Optimizer — 用户意图解析与 Prompt 优化

## 概述

在用户提交分析请求后、正式进入 Phase 0 Domain Anchoring 之前，本 Skill 负责：

1. **数据路径探测** — 读取用户提供的路径，检查文件结构和数据类型
2. **意图解析** — 从用户自然语言中提取分析目标、数据类型、期望产出
3. **Prompt 优化** — 将模糊请求转化为结构化、完整的分析规格说明
4. **用户确认** — 将优化后的 Prompt 返回用户，等待确认后再继续
5. **锚点初始化** — 确认后的信息直接注入 Phase 0 的 project-anchor.yaml

## 触发条件

```
用户发送新分析请求时（以下任一）：
  ├── "帮我分析这批数据 /path/to/data"
  ├── "做一下 16S 分析"
  ├── "分析一下差异表达"
  ├── 任何包含分析意图 + 数据路径的消息
  └── 用户通过 /bio-analyze 命令发起分析
```

## 核心流程

```
用户输入原始 Prompt
  │
  ├── Step 1: 数据路径探测
  │   ├── 识别用户消息中的路径（绝对路径 / 相对路径）
  │   ├── ls / tree 检查路径结构
  │   ├── 识别文件类型（.fastq.gz, .bam, .h5ad, .csv, .tsv, ...）
  │   ├── 统计样本数量、文件大小
  │   ├── 查找 metadata 文件（metadata.csv/tsv, sample_info.*, manifest.*)
  │   └── 输出: data_summary（数据类型、样本量、文件列表）
  │
  ├── Step 2: 意图解析
  │   ├── 从用户消息中提取:
  │   │   ├── 分析类型（16S/shotgun/scRNA/bulk RNA/WGS/...）
  │   │   ├── 分析目标（差异分析/聚类/富集/通路分析/...）
  │   │   ├── 物种信息（human/mouse/...）
  │   │   ├── 实验设计（分组/对照/时间序列/...）
  │   │   ├── 特殊要求（特定工具/特定数据库/特定参数）
  │   │   └── 输出偏好（报告语言/图表风格/输出格式）
  │   ├── 交叉验证: 数据文件类型 vs 用户声称的分析类型
  │   │   ├── .fastq.gz + "16S" → ✅ 一致
  │   │   ├── .h5ad + "16S" → ⚠️ 冲突，提醒用户
  │   │   └── 无法确定 → 列出可能性，请求用户澄清
  │   └── 输出: intent_summary（结构化意图摘要）
  │
  ├── Step 3: Prompt 优化
  │   ├── 信息补全 — 检查必要信息是否完整:
  │   │   ├── ✅ 必须有: 数据类型 + 数据路径 + 分析目标
  │   │   ├── ⚠️ 推荐有: 物种 + 分组信息 + 测序平台
  │   │   └── 💡 可选有: 特定工具偏好 + 参数要求 + 输出格式
  │   ├── 结构化重组 — 将信息组织为标准格式
  │   ├── 歧义消解 — 识别并标注模糊或矛盾之处
  │   └── 输出: optimized_prompt（优化后的结构化 Prompt）
  │
  ├── Step 4: 用户确认
  │   ├── 展示优化后的 Prompt（结构化表格 + 中英对照术语）
  │   ├── 标注自动推断的信息（以 🔍 标记）
  │   ├── 标注缺失但推荐补充的信息（以 ❓ 标记）
  │   ├── 等待用户确认或修改
  │   └── 用户确认 → 进入 Phase 0
  │
  └── Step 5: 注入 Phase 0
      ├── 将确认后的信息写入 project-anchor.yaml 初始化数据
      └── 触发 omics-router 进行组学类型路由
```

## 优化后 Prompt 输出模板

```markdown
## 📋 分析规格确认书 (Analysis Specification)

### 1. 数据概况 (Data Summary)
| 项目 | 信息 |
|------|------|
| 数据路径 | `/path/to/data/` |
| 数据类型 | 16S amplicon (paired-end .fastq.gz) |
| 样本数量 | 24 (12 treatment + 12 control) 🔍 |
| 测序平台 | Illumina MiSeq 2×300bp 🔍 |
| 物种来源 | Human gut microbiome |
| Metadata | `metadata.tsv` (已找到) ✅ |

### 2. 分析目标 (Analysis Objectives)
- [x] 物种多样性分析 (Alpha + Beta diversity)
- [x] 差异物种分析 (LEfSe / ANCOM-BC)
- [x] 功能预测 (PICRUSt2)
- [ ] 网络分析 ❓ (建议: 如果需要微生物互作网络，请确认)

### 3. 分析配置 (Configuration)
| 配置项 | 值 | 备注 |
|--------|-----|------|
| 执行模式 | semi-auto | ❓ 请确认: auto / semi-auto / interactive |
| 运行环境 | 待检测 | Phase 0 自动检测 HPC/本地 |
| 报告语言 | 中文 | 🔍 根据用户输入语言推断 |
| 分析路线 | Type A (Amplicon) | 🔍 根据数据类型推断 |

### 4. 自动推断信息 (Auto-Inferred) 🔍
- 测序平台: 根据 read 长度推断为 Illumina MiSeq
- 样本分组: 根据 metadata.tsv 中 "group" 列推断

### 5. 待确认信息 ❓
- 是否需要宿主序列去除？(human gut 样本建议开启)
- 分析路线确认: 仅 amplicon 还是需要 shotgun 联合分析？
- 执行模式选择: auto(无人值守) / semi-auto(关键节点停下) / interactive(每步确认)

---
✅ 如果以上信息正确，请回复 **"确认"** 或 **"开始分析"** 即可继续。
❌ 如需修改，请直接告诉我需要调整的内容。
```

## 数据路径探测规则

### 路径识别策略

```
输入文本解析:
  ├── 绝对路径: /home/user/data/, /data/project/, D:\data\...
  ├── 相对路径: ./data/, ../raw_data/, data/
  ├── 环境变量: $HOME/data, ${WORKDIR}/fastq
  └── 通配符: /path/to/*.fastq.gz, /path/to/sample_*
```

### 文件类型识别表

| 文件后缀 | 推断数据类型 | 推荐组学 |
|----------|-------------|---------|
| `.fastq.gz`, `.fq.gz` | 原始测序数据 | metagenome / transcriptome / genomics |
| `.bam`, `.cram` | 比对结果 | genomics / transcriptome |
| `.h5ad`, `.h5`, `.loom` | 单细胞矩阵 | scrna |
| `.mtx` + `barcodes.tsv` | 10X Chromium | scrna |
| `.csv`, `.tsv`, `.xlsx` | 表格数据 | 需进一步判断 |
| `.vcf`, `.vcf.gz` | 变异文件 | genomics |
| `.mzML`, `.mzXML`, `.raw` | 质谱数据 | proteomics / metabolomics |
| `.bed`, `.bedGraph`, `.bigWig` | 基因组区间 | epigenomics |
| `.h5seurat`, `.rds` | Seurat 对象 | scrna |

### Metadata 自动发现

```
在数据目录中搜索:
  ├── metadata.csv / metadata.tsv / metadata.xlsx
  ├── sample_info.* / sample_sheet.*
  ├── manifest.* / mapping_file.*
  ├── coldata.* / phenodata.*
  └── 任何包含 "sample", "group", "condition" 列的表格文件

如果找到 metadata:
  ├── 读取前 5 行预览
  ├── 识别分组列 (group, condition, treatment, ...)
  ├── 统计分组信息 (样本数 per group)
  └── 检查样本 ID 与数据文件的对应关系
```

## 意图解析模板

### 关键词映射表

| 用户关键词 | 解析为 |
|-----------|--------|
| "16S", "扩增子", "amplicon" | 宏基因组 - 扩增子分析 |
| "宏基因组", "shotgun", "全基因组测序" | 宏基因组 - 鸟枪法测序 |
| "单细胞", "scRNA", "10X", "Chromium" | 单细胞 RNA-seq |
| "转录组", "RNA-seq", "差异表达", "DEG" | Bulk 转录组 |
| "基因组", "WGS", "WES", "变异", "突变" | 基因组学 |
| "蛋白质组", "质谱", "TMT", "DIA" | 蛋白质组学 |
| "代谢组", "LC-MS", "代谢物" | 代谢组学 |
| "ATAC-seq", "ChIP-seq", "甲基化" | 表观基因组学 |
| "TCR", "BCR", "免疫组库" | 免疫组库 |
| "空间转录组", "Visium", "MERFISH" | 空间组学 |

### 歧义处理规则

<IRON-LAW>
当数据类型与用户描述存在冲突时:
1. 以实际数据文件类型为准（磁盘为真）
2. 明确告知用户检测到的冲突
3. 列出两种可能的解读
4. 等待用户澄清后再继续
5. NEVER 静默忽略冲突
</IRON-LAW>

## 迭代优化机制

如果用户对初次优化结果不满意，支持迭代修改:

```
用户: "不对，我要的是 shotgun 不是 16S"
  │
  ├── 更新 data_type: "shotgun-metagenome"
  ├── 重新评估分析路线: Type R (Read-based) 或 Type M (Assembly)
  ├── 更新推荐工具: MetaPhlAn4/HUMAnN3 或 MEGAHIT/MetaSPAdes
  └── 重新展示优化后 Prompt，等待再次确认

最多迭代 3 次自动优化，之后直接使用用户最新输入
```

## 与后续 Phase 的衔接

```
Prompt 优化完成 + 用户确认
  │
  ├── 写入 optimized-prompt.yaml 到 docs/ 目录
  │   ├── original_prompt: "用户原始输入"
  │   ├── optimized_prompt: "结构化优化后版本"
  │   ├── data_summary: { ... }
  │   ├── intent_summary: { ... }
  │   └── user_confirmed: true
  │
  ├── 路由到正确的 Agent (通过 omics-router)
  │   └── 已知数据类型 → 直接路由，无需再次询问
  │
  └── Phase 0 Domain Anchoring
      └── 已有完整信息 → 快速创建 project-anchor.yaml
      └── 避免 Phase 0 中重复询问用户已确认的信息
```

## 质量检查清单

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | 数据路径是否存在且可访问 | `ls` 命令成功 |
| 2 | 文件类型是否与声称一致 | 后缀匹配 |
| 3 | Metadata 是否被找到和解析 | 分组信息提取成功 |
| 4 | 分析目标是否明确 | 至少 1 个具体目标 |
| 5 | 数据-目标一致性 | 数据类型支持目标分析 |
| 6 | 优化 Prompt 是否展示给用户 | 必须展示并等待确认 |
| 7 | 用户是否明确确认 | "确认"/"开始"/"OK" 等 |

## 红线信号

| 信号 | 处理 |
|------|------|
| 数据路径不存在 | ⛔ 停止，请求用户提供正确路径 |
| 目录为空 | ⛔ 停止，请求用户确认路径 |
| 数据类型无法识别 | ⚠️ 列出文件列表，请求用户说明 |
| 数据与意图严重冲突 | ⚠️ 明确告知冲突，等待澄清 |
| 未经用户确认就开始分析 | ⛔ 违反流程，必须先确认 |

## 开发指南

### 集成方式

本 Skill 作为 **Pre-Phase** 插入到分析流程中:

```
原流程: 用户输入 → omics-router → Phase 0 → ...
新流程: 用户输入 → prompt-optimizer → 用户确认 → omics-router → Phase 0 → ...
```

### Agent Prompt 集成代码

在各领域 Agent 的 prompt 中添加:

```markdown
## Pre-Phase: Prompt Optimization

<IRON-LAW>
When receiving a NEW analysis request (not resuming):
1. Load `prompt-optimizer` skill IMMEDIATELY
2. Follow the data exploration → intent parsing → prompt optimization flow
3. Present the optimized Analysis Specification to the user
4. WAIT for explicit user confirmation before proceeding to Phase 0
5. Do NOT skip this step — even if the user's request seems clear
</IRON-LAW>
```

### Skill 路由表更新

在所有 Agent 的 Skill 路由表中添加:

```markdown
| Phase | 领域专有 Skill | 共享框架 Skill |
|-------|---------------|---------------|
| Pre   | —             | `prompt-optimizer` ● |
| 0     | ...           | ...           |
```

### 实现优先级

| 步骤 | 内容 | 优先级 |
|------|------|:------:|
| 1 | SKILL.md 文件（本文件） | **P0** |
| 2 | 集成到 metagenome-expert Agent prompt | **P0** |
| 3 | 集成到 scrna-expert Agent prompt | **P0** |
| 4 | 集成到 transcriptome-expert Agent prompt | **P0** |
| 5 | optimized-prompt.yaml 模板 | **P0** |
| 6 | 其余领域 Agent 集成 | **P1** |
