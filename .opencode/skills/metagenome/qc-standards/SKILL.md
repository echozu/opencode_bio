---
name: qc-standards
description: Use when assessing or executing quality control — enforces minimum quality thresholds for reads, assemblies, annotations, and all intermediate outputs in metagenome analysis
---

# QC Standards (Discipline Layer)

## Overview

Quality control is the foundation of metagenome analysis. Poor-quality data produces unreliable results regardless of how sophisticated the downstream analysis is. This skill defines minimum quality thresholds that must be met.

**Core principle:** Quality cannot be added later. It must be verified upfront.

## The Iron Law

<IRON-LAW>
ALL DATA MUST MEET MINIMUM QUALITY THRESHOLDS BEFORE PROCEEDING TO ANALYSIS.
Samples that fail QC must be flagged, not silently excluded or silently included.
The user decides what to do with failed samples — not the AI.
</IRON-LAW>

## Minimum Quality Thresholds

### Read Quality (All Data Types)

| Metric | Threshold | Action if Failed |
|--------|-----------|-----------------|
| Per-base quality | Median ≥Q20 at all positions | Investigate; may need trimming adjustment |
| Adapter content | <1% after trimming | Re-run adapter removal |
| Read length (post-QC) | ≥100bp (amplicon), ≥50bp (shotgun) | Adjust trimming parameters |
| Duplication rate | <50% (shotgun) | Flag; may indicate library prep issue |
| N content | <5% | Flag; may indicate sequencing quality issue |

### Sequencing Depth

| Data Type | Minimum per Sample | Recommended | Action if Below |
|-----------|-------------------|-------------|----------------|
| 16S amplicon | 1,000 reads post-QC | 10,000+ | Flag; exclude from diversity if <1,000 |
| Shotgun (taxonomy) | 100,000 reads | 1,000,000+ | Flag; may miss low-abundance species |
| Shotgun (function) | 500,000 reads | 5,000,000+ | Flag; HUMAnN unreliable below this |
| Shotgun (assembly) | 1,000,000 reads | 10,000,000+ | Flag; assembly will be fragmented |

### Host DNA Contamination (Human Gut)

| Level | Threshold | Action |
|-------|-----------|--------|
| Acceptable | <5% human reads | Proceed |
| Warning | 5-20% human reads | Flag; recommend deeper host removal |
| Critical | >20% human reads | STOP; host removal mandatory before proceeding |

### Assembly Quality (Type M)

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| N50 | 500bp | 5,000bp | 50,000bp |
| Total assembly | 10Mb | 100Mb | 500Mb |
| Mapping rate | 30% | 60% | 80% |

### MAG Quality (Type M — MIMAG Standards)

| Quality Level | Completeness | Contamination | Use in Analysis |
|--------------|-------------|---------------|-----------------|
| High | >90% | <5% | Primary analysis |
| Medium | ≥50% | <10% | Secondary/supporting |
| Low | <50% | >10% | Exclude from primary |

### Profiling Quality (Type R)

| Metric | Minimum | Warning | Good |
|--------|---------|---------|------|
| MetaPhlAn mapped reads | 20% | 20-50% | >50% |
| HUMAnN gene mapping | 20% | 20-40% | >40% |
| Species detected | 10 | 10-50 | >50 |

## Quality Check at Every Stage

| Pipeline Stage | Quality Check | What to Look For |
|---------------|---------------|-----------------|
| Raw data received | File integrity, sample count | Corrupted files, missing samples |
| Post-QC | Read quality, depth, adapters | Depth loss >50%, adapter residual |
| Post-host-removal | Host DNA % | >5% residual human reads |
| Post-denoising | ASV count, chimera rate | >50% read loss, >25% chimeras |
| Post-assembly | N50, mapping rate | N50 <500, mapping <30% |
| Post-profiling | Mapping rate, species count | <20% mapped, <10 species |
| Post-differential | Significant features, effect sizes | 0 significant or >1000 significant |

## Red Flags — STOP

- Proceeding with analysis when samples fail minimum thresholds
- Not checking quality at intermediate pipeline stages
- Silently excluding failed samples without documentation
- Using "standard" thresholds without checking data characteristics
- Ignoring contamination indicators

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "QC looks fine overall" | Check EVERY sample individually. Aggregates hide outliers. |
| "Low depth samples add diversity" | Low depth samples add noise, not diversity. Flag them. |
| "Host contamination won't affect taxonomy" | Human DNA wastes sequencing capacity and can confuse classifiers. Remove it. |
| "The assembly N50 is typical for metagenomes" | Typical ≠ sufficient. Check if N50 supports your analysis goals. |
| "FastQC is enough" | FastQC is the start. Check contamination, depth, and domain-specific metrics too. |
| "We can't exclude samples, the study is small" | Small studies need HIGH quality per sample. One bad sample can skew everything. |
