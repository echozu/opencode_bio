---
name: cell-translation
description: >
  Analyze biological cellular translation (mRNA → protein synthesis) processes.
  Use when performing Ribo-seq / ribosome profiling analysis, translation efficiency (TE)
  calculation, codon usage analysis, ORF prediction, translational regulation study,
  or integrating Ribo-seq with RNA-seq/proteomics data. Covers the full pipeline from
  ribosome footprint processing to translational landscape characterization.
---

# Cell Translation — 细胞翻译过程分析 (mRNA → Protein)

## 概述

本 Skill 聚焦于**细胞翻译过程**（mRNA → Protein）的生物信息学分析，涵盖核糖体图谱分析
（Ribo-seq / Ribosome Profiling）、翻译效率计算、密码子使用分析、ORF 预测、翻译调控研究等。

## 适用场景

```
触发条件（以下任一）：
  ├── 用户提到 "Ribo-seq"、"ribosome profiling"、"核糖体图谱"
  ├── 用户提到 "翻译效率"、"translation efficiency"、"TE"
  ├── 用户提到 "密码子使用"、"codon usage"、"CUB"
  ├── 用户提到 "ORF 预测"、"open reading frame"、"uORF"
  ├── 用户需要分析 "翻译调控"、"translational regulation"
  ├── 用户提到 "核糖体足迹"、"ribosome footprint"、"RPF"
  ├── 用户需要整合 Ribo-seq + RNA-seq 数据
  └── 用户提到 "多聚核糖体"、"polysome profiling"
```

## 核心分析类型

| 类型 | 说明 | 核心数据 | 典型产出 |
|------|------|---------|---------|
| **Type R (Ribo-seq)** | 核糖体图谱全转录组翻译分析 | Ribo-seq .fastq.gz | 翻译景观图、基因级 TE |
| **Type T (TE Analysis)** | 翻译效率差异分析 | Ribo-seq + RNA-seq paired | 差异翻译基因列表 |
| **Type C (Codon)** | 密码子使用偏好分析 | CDS 序列 / Ribo-seq | 密码子适应指数、tAI |
| **Type O (ORF Discovery)** | 新 ORF / uORF 发现 | Ribo-seq + 参考基因组 | 非经典翻译事件 |
| **Type I (Integration)** | 多组学翻译调控整合 | Ribo-seq + RNA-seq + Proteomics | 转录-翻译-蛋白协调性 |

---

## Ribo-seq 分析流程

### Phase 1: 数据预处理

```
Raw Ribo-seq reads (.fastq.gz)
  │
  ├── Step 1: 接头去除与质控
  │   ├── 工具: fastp / Cutadapt / Trim Galore
  │   ├── 关键: Ribo-seq reads 通常 26-34 nt
  │   ├── 去除 3' adapter (必须，RPF 短片段)
  │   └── 质量过滤: Q ≥ 20, 长度过滤: 26-34 nt
  │
  ├── Step 2: rRNA 去除
  │   ├── 工具: Bowtie2 / SortMeRNA
  │   ├── 比对到 rRNA 参考序列
  │   ├── 保留未比对 reads (non-rRNA)
  │   └── 期望: rRNA 占比应 < 30% (好的文库 < 10%)
  │
  ├── Step 3: 比对到参考基因组/转录组
  │   ├── 工具: STAR / Bowtie2 / HISAT2
  │   ├── 参数: 不允许多重比对 (--outFilterMultimapNmax 1)
  │   ├── 输出: BAM (sorted, indexed)
  │   └── 期望: 唯一比对率 ≥ 60%
  │
  └── Step 4: RPF 长度分布检查
      ├── 统计 mapped reads 的长度分布
      ├── 期望: 主峰在 28-30 nt (哺乳动物)
      ├── 三核苷酸周期性验证 (triplet periodicity)
      └── 如果无清晰主峰 → ⚠️ 文库质量警告
```

<IRON-LAW>
Ribo-seq 数据预处理铁律:
1. RPF 长度过滤是 MANDATORY 的 — 不在 26-34 nt 范围内的 reads 必须去除
2. rRNA 去除必须在基因组比对之前完成
3. 三核苷酸周期性 (3-nt periodicity) 必须被验证 — 这是 Ribo-seq 数据质量的金标准
4. 如果三核苷酸周期性不明显，STOP 并报告给用户，讨论数据质量问题
5. P-site offset 校正必须在任何下游分析之前完成
</IRON-LAW>

### Phase 2: P-site Offset 校正

```
P-site (peptidyl site) 偏移量校正:
  │
  ├── 目的: 将 RPF 5'端映射位置校正到核糖体 P-site 位置
  │
  ├── 方法 1: 起始密码子法 (推荐)
  │   ├── 统计 RPF 5'端相对于 AUG 起始密码子的距离分布
  │   ├── 不同长度 RPF 的 offset 可能不同
  │   ├── 28 nt RPF → 典型 offset = 12 nt
  │   ├── 29 nt RPF → 典型 offset = 12 nt
  │   └── 30 nt RPF → 典型 offset = 13 nt
  │
  ├── 方法 2: 终止密码子法 (辅助验证)
  │   └── RPF 密度在终止密码子处应有明显下降
  │
  ├── 工具:
  │   ├── RiboCode — 自动 P-site offset 校正
  │   ├── Ribotricer — P-site 推断 + 周期性分析
  │   ├── plastid (Python) — metagene 分析 + offset 推断
  │   └── riboWaltz (R) — P-site 优化 + 可视化
  │
  └── 验证: 校正后 P-site 密度在 CDS 内呈三核苷酸周期性
```

### Phase 3: 翻译景观分析

```
Metagene 分析 (核心质控图):
  │
  ├── 起始密码子周围 metagene profile
  │   ├── 以 AUG 为中心, ±50 codons
  │   ├── 期望: AUG 处有明显的 RPF 密度峰
  │   └── 5'UTR 区域应有极低密度 (除非有 uORF)
  │
  ├── 终止密码子周围 metagene profile
  │   ├── 以 stop codon 为中心, ±50 codons
  │   └── 期望: 终止密码子处密度骤降
  │
  ├── CDS 区域密度分布
  │   ├── 全长 CDS (normalized to % length)
  │   ├── 5'UTR / CDS / 3'UTR 密度占比
  │   └── 期望: > 80% reads 映射到 CDS
  │
  └── 可视化:
      ├── 工具: riboWaltz, plastid, RiboProfiling
      ├── 输出: metagene plots (PDF/SVG)
      └── 与 figure Skill 协作生成出版级图表
```

### Phase 4: 翻译效率 (TE) 计算

```
Translation Efficiency (TE) = Ribo-seq RPF density / RNA-seq mRNA abundance

定量方式:
  │
  ├── 基因级定量:
  │   ├── Ribo-seq: 统计 CDS 区域 RPF counts (排除起始/终止 ±15 codons)
  │   ├── RNA-seq: 统计全长转录本 counts
  │   ├── 标准化: RPKM / TPM / CPM
  │   └── TE = RPF_RPKM / mRNA_RPKM
  │
  ├── 差异翻译效率分析 (Differential TE):
  │   ├── 工具: Xtail (推荐, 专为 Ribo-seq 设计)
  │   │   ├── 输入: Ribo-seq counts + RNA-seq counts (matched samples)
  │   │   ├── 模型: 同时考虑 mRNA 和 RPF 变化
  │   │   └── 输出: log2FC_TE, p-value, FDR
  │   ├── 工具: RiboDiff
  │   │   ├── 基于广义线性模型 (GLM)
  │   │   └── 适合复杂实验设计
  │   ├── 工具: deltaTE (简单法)
  │   │   ├── 分别做 RNA-seq 和 Ribo-seq 的 DESeq2
  │   │   └── deltaTE = log2FC_Ribo - log2FC_RNA
  │   └── 工具: anota2seq
  │       ├── 贝叶斯方法
  │       └── 区分翻译调控 vs 转录调控 vs 缓冲效应
  │
  └── 关键阈值:
      ├── |log2FC_TE| ≥ 1 且 FDR < 0.05 → 显著差异翻译
      ├── TE ↑ + mRNA 不变 → 翻译上调 (translational upregulation)
      ├── TE ↓ + mRNA 不变 → 翻译抑制 (translational repression)
      └── TE 不变 + mRNA ↑ → 转录调控 (transcriptional regulation)
```

<IRON-LAW>
翻译效率分析铁律:
1. TE 计算必须使用 matched RNA-seq 和 Ribo-seq 数据 (同一样本/同一批次)
2. RPF counts 只统计 CDS 区域，排除起始/终止密码子附近 (±15 codons)
3. 差异 TE 分析不能简单用 TE 值做 t-test — 必须使用专用工具 (Xtail/RiboDiff/anota2seq)
4. 报告差异翻译基因时，必须同时报告 mRNA 和 RPF 的变化方向
5. 需要区分四种调控模式: 翻译上调、翻译抑制、转录调控、缓冲效应
</IRON-LAW>

### Phase 5: 高级翻译分析

#### 5.1 密码子使用分析 (Codon Usage)

```
密码子级别翻译速度分析:
  │
  ├── 密码子占用率 (Codon Occupancy):
  │   ├── 统计每个密码子位置的 RPF P-site 密度
  │   ├── 密码子停滞指数 (Codon Stalling Index)
  │   └── 与 tRNA 丰度的相关性 (tRNA Adaptation Index, tAI)
  │
  ├── 分析工具:
  │   ├── codonDT (R) — 密码子级 Ribo-seq 分析
  │   ├── iCodon — 密码子优化度计算
  │   ├── EMBOSS cusp/chips — 经典密码子使用分析
  │   └── CodonW — 密码子使用统计
  │
  ├── 可视化:
  │   ├── 密码子热图 (64 codons × samples)
  │   ├── A-site / P-site / E-site 占用率比较
  │   └── 慢速密码子 vs 快速密码子分布
  │
  └── 生物学意义:
      ├── 翻译暂停位点 (ribosome pausing)
      ├── 共翻译折叠 (co-translational folding) 信号
      └── 翻译速率与蛋白质折叠质量的关系
```

#### 5.2 ORF 发现 (非经典翻译事件)

```
Ribo-seq 引导的新 ORF 发现:
  │
  ├── 上游 ORF (uORF):
  │   ├── 定义: 5'UTR 中的 AUG 起始的短 ORF
  │   ├── 功能: 调控主 ORF 的翻译 (通常是抑制)
  │   ├── 检测: RPF 在 5'UTR 中呈三核苷酸周期性
  │   └── 工具: RiboCode, ORFquant, Ribo-TISH
  │
  ├── 下游 ORF (dORF):
  │   ├── 定义: 3'UTR 中的翻译事件
  │   ├── 检测: RPF 在 3'UTR 中有显著富集
  │   └── 通常与 readthrough 或内部起始相关
  │
  ├── 非 AUG 起始的 ORF:
  │   ├── 近同源起始密码子: CUG, GUG, UUG
  │   ├── 工具: RiboCode (支持非 AUG 搜索)
  │   └── 需要特殊参数设置
  │
  ├── 长非编码 RNA (lncRNA) 的翻译:
  │   ├── 部分 lncRNA 实际编码微肽 (micropeptide)
  │   ├── 检测: RPF 映射到 lncRNA 且有周期性
  │   └── 生物学意义: 功能性微肽发现
  │
  └── 工具对比:
      | 工具 | 特点 | 输入 |
      |------|------|------|
      | RiboCode | 三核苷酸周期性 + 统计检验 | BAM + GTF |
      | ORFquant | 转录本级 ORF 定量 | BAM + 转录组 |
      | Ribo-TISH | 多种起始位点检测 | BAM + GTF |
      | RiboTaper | 多重周期性检验 | BAM + GTF |
      | Ribotricer | 快速 ORF 检测 | BAM + GTF |
```

#### 5.3 翻译调控机制分析

```
常见翻译调控机制的检测:
  │
  ├── mTOR 通路相关:
  │   ├── TOP mRNA (5' Terminal OligoPyrimidine) 翻译调控
  │   ├── 4E-BP1 / eIF4E 依赖的翻译
  │   └── GSEA 分析 TOP mRNA 基因集的 TE 变化
  │
  ├── 应激颗粒 (Stress Granules) 相关:
  │   ├── eIF2α 磷酸化导致的全局翻译抑制
  │   ├── uORF 介导的选择性翻译上调 (如 ATF4)
  │   └── 检测: 全局 TE 下降 + 特定基因 TE 上升
  │
  ├── miRNA 介导的翻译抑制:
  │   ├── miRNA target 基因的 TE 变化
  │   ├── 整合 miRNA 表达谱数据
  │   └── 工具: TargetScan + TE 关联分析
  │
  ├── RNA 结构介导的翻译调控:
  │   ├── IRES (Internal Ribosome Entry Site) 依赖翻译
  │   ├── G-quadruplex 结构影响翻译
  │   └── 整合 RNA 结构数据 (DMS-seq / SHAPE-seq)
  │
  └── 共翻译事件:
      ├── 核糖体碰撞 (ribosome collision) — disome profiling
      ├── 共翻译蛋白质折叠
      └── 共翻译膜插入 (SRP 依赖)
```

### Phase 6: 多组学翻译调控整合

```
三层整合分析 (Transcription → Translation → Protein):
  │
  ├── 转录-翻译协调性:
  │   ├── mRNA 变化 vs RPF 变化散点图
  │   ├── 四象限分类:
  │   │   ├── Q1: mRNA↑ + RPF↑ = 转录驱动 (homodirectional)
  │   │   ├── Q2: mRNA↓ + RPF↑ = 翻译特异上调
  │   │   ├── Q3: mRNA↑ + RPF↓ = 翻译特异抑制 (buffering)
  │   │   └── Q4: mRNA↓ + RPF↓ = 转录驱动 (homodirectional)
  │   └── 工具: anota2seq (最佳), 自定义 R 脚本
  │
  ├── 翻译-蛋白质验证:
  │   ├── TE 变化 vs 蛋白质丰度变化 相关性
  │   ├── 翻译上调但蛋白质无变化 → 蛋白质降解活跃
  │   └── 工具: 自定义整合分析脚本
  │
  ├── 通路级翻译调控:
  │   ├── GSEA 使用 TE 排序的基因列表
  │   ├── GO/KEGG 富集分析 (差异翻译基因)
  │   └── 翻译调控网络构建
  │
  └── 可视化 (与 figure Skill 协作):
      ├── mRNA vs RPF 散点图 (四象限着色)
      ├── TE 变化火山图
      ├── 翻译景观浏览器截图 (IGV / GWIPS-viz)
      ├── metagene profiles (多条件叠加)
      └── 密码子停滞热图
```

## 工具汇总表

| 工具 | 功能 | 语言 | 阶段 |
|------|------|------|------|
| fastp / Cutadapt | 接头去除 + 质控 | Python/C++ | Phase 1 |
| Bowtie2 / SortMeRNA | rRNA 去除 | C++ | Phase 1 |
| STAR / HISAT2 | 基因组比对 | C++ | Phase 1 |
| riboWaltz | P-site offset + metagene | R | Phase 2-3 |
| plastid | metagene + P-site | Python | Phase 2-3 |
| RiboCode | ORF 检测 + P-site | Python | Phase 2, 5 |
| Ribotricer | 周期性分析 + ORF | Python | Phase 2, 5 |
| Xtail | 差异 TE 分析 | R | Phase 4 |
| RiboDiff | 差异 TE (GLM) | Python | Phase 4 |
| anota2seq | 翻译调控分类 | R | Phase 4, 6 |
| deltaTE | 差异 TE (简单法) | R | Phase 4 |
| codonDT | 密码子级分析 | R | Phase 5 |
| ORFquant | 转录本级 ORF 定量 | R | Phase 5 |
| Ribo-TISH | 起始位点检测 | Python | Phase 5 |

## QC 标准

| 指标 | 优秀 | 合格 | 不合格 |
|------|------|------|--------|
| rRNA 占比 | < 10% | < 30% | ≥ 30% |
| RPF 长度主峰 | 28-30 nt 清晰单峰 | 有可辨识主峰 | 无明显主峰 |
| 三核苷酸周期性 | 明显 (frame 0 > 70%) | 可见 (frame 0 > 50%) | 不明显 |
| CDS 区域占比 | > 80% | > 60% | < 60% |
| 唯一比对率 | > 70% | > 50% | < 50% |
| 起始密码子富集 | 明显峰值 | 可见峰值 | 无峰值 |

## 红线信号

| 信号 | 处理 |
|------|------|
| 三核苷酸周期性不明显 | ⛔ 停止分析，报告数据质量问题 |
| RPF 长度无清晰主峰 | ⛔ 停止，可能不是 Ribo-seq 数据 |
| CDS 区域占比 < 60% | ⚠️ 警告用户，结果可能不可靠 |
| RNA-seq 与 Ribo-seq 样本不匹配 | ⛔ 不能做 TE 分析，请求匹配数据 |
| TE 做 t-test 而非专用工具 | ⛔ 方法错误，必须使用 Xtail/RiboDiff/anota2seq |
| 未排除起始/终止区域的 RPF counts | ⚠️ TE 计算可能有偏差 |

## 借口拦截表

| 借口 | 现实 |
|------|------|
| "三核苷酸周期性差一点也行" | 周期性是数据有效性的核心证据，不可妥协 |
| "直接用全长转录本算 RPF" | RPF 只应统计 CDS 区域，5'UTR/3'UTR 有不同生物学意义 |
| "TE 的 fold change 用 t-test 足够" | TE 是比值，需要特殊统计模型处理 |
| "rRNA 去不干净也没关系" | rRNA reads 浪费测序深度，影响定量准确性 |
| "P-site offset 都用 12" | 不同长度 RPF 的 offset 不同，必须实验确定 |
| "uORF 分析不重要" | uORF 是翻译调控的关键机制，忽略则丢失重要信息 |

## 与其他 Skill 的协作

```
cell-translation Skill 在分析流程中的位置:
  │
  ├── 输入依赖:
  │   ├── qc-grading-framework → 数据质量分级
  │   ├── figure → 图表生成 + 质量标准
  │   └── statistical-testing-framework → 统计检验框架
  │
  ├── 协作 Skill:
  │   ├── figure → 生成 metagene plots, TE 火山图, 密码子热图
  │   ├── enrichment-framework → 差异翻译基因的 GO/KEGG 富集
  │   ├── reproducibility-discipline → 工具版本锁定, 参数记录
  │   └── report-generation-framework → 翻译分析报告章节
  │
  └── 下游应用:
      ├── 翻译调控机制发现
      ├── 药物靶点 (翻译相关) 发现
      ├── 非编码 RNA 翻译功能验证
      └── 蛋白质组学数据验证
```

## 开发指南

### 集成方式

本 Skill 作为**领域专有 Skill** 或**共享 Skill** 集成到分析流程中：

```
适用 Agent:
  ├── transcriptome-expert → Ribo-seq 作为转录组的翻译层分析
  ├── genomics-expert → ORF 预测与基因注释增强
  ├── proteomics-expert → 翻译-蛋白质组整合验证
  └── multi-omics-orchestrator → 多组学翻译调控分析
```

### Skill 路由表位置

```
| Phase | Skill |
|-------|-------|
| 1     | `cell-translation` ○ (当数据包含 Ribo-seq 时) |
| 4     | `cell-translation` ● (核心翻译分析) |
| 5     | `cell-translation` ○ (高级翻译调控分析) |
| 6     | `cell-translation` ○ (翻译分析报告整合) |
```

### 实现优先级

| 步骤 | 内容 | 优先级 |
|------|------|:------:|
| 1 | SKILL.md 文件（本文件） | **P0** |
| 2 | 集成到 transcriptome-expert Agent prompt | **P1** |
| 3 | Ribo-seq QC 阈值与 qc-grading-framework 对接 | **P1** |
| 4 | TE 分析工具推荐表扩充 | **P1** |
| 5 | 密码子分析可视化模板 | **P2** |
| 6 | 多组学整合分析流程完善 | **P2** |
