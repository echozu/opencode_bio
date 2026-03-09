---
name: reproducibility-discipline
description: "DISCIPLINE SKILL — active from Phase 1 onward for ALL omics analysis. Enforces reproducibility: tool version locking, parameter documentation, command logging, database version tracking, and anti-cherry-picking. Works alongside file checkpoint protocol."
---

# Reproducibility Discipline — Bioinformatics Analysis

## The Iron Law

```
NO ANALYSIS STEP WITHOUT VERSIONED TOOLS, LOGGED COMMANDS, AND DOCUMENTED PARAMETERS.
```

This skill is active for every computational task in omics analysis. Core rules are embedded in all Agent prompts; this Skill provides the detailed execution steps and checklists.

## 1. The HBEVI Cycle (Adapted for Bioinformatics)

Every analysis unit follows: **HYPOTHESIZE → BASELINE → EXPERIMENT → VERIFY → INTERPRET**.

### 1.1 HYPOTHESIZE
- State what you expect from this analysis step and why
- Example: "We expect samples to cluster by treatment group after batch correction. If not, batch effects may dominate."

### 1.2 BASELINE
- Establish reference points before running analysis:
  - Known QC thresholds for this data type
  - Expected ranges from literature or pilot data
  - Previous analysis results (if re-analysis)

### 1.3 EXPERIMENT
- Execute the analysis with full controls (see §2–4 below)

### 1.4 VERIFY
- Check results against expectations:
  - Output files exist and are non-empty
  - Values fall within expected ranges
  - QC metrics meet grade thresholds

### 1.5 INTERPRET
- Record findings — both positive AND negative:
  - Hypothesis supported → record evidence with specific metrics
  - Hypothesis refuted → record what was learned
  - Ambiguous → state what additional analysis would resolve it

## 2. Tool Version Locking

<IRON-LAW>
Every tool used MUST have its version recorded in the checkpoint file.

### Recording Commands:
```bash
# Conda environment
conda list > docs/{domain}/env/conda_packages.txt
conda env export > docs/{domain}/env/environment.yaml

# pip packages
pip freeze > docs/{domain}/env/pip_requirements.txt

# R session
Rscript -e 'writeLines(capture.output(sessionInfo()), "docs/{domain}/env/r_session_info.txt")'

# Individual tools
fastp --version 2>&1 | head -1
STAR --version
samtools --version | head -1
```

### Checkpoint Format:
```yaml
tools_used:
  - name: "fastp"
    version: "0.23.4"
    command: "fastp -i raw_R1.fq.gz -I raw_R2.fq.gz -o clean_R1.fq.gz -O clean_R2.fq.gz --thread 16"
  - name: "STAR"
    version: "2.7.11a"
    command: "STAR --runMode alignReads --genomeDir /ref/star_index ..."
```
</IRON-LAW>

## 3. Database Version Tracking

<IRON-LAW>
Databases evolve. Different versions give different results. MUST record:

| Database | Version Example | How to Check |
|----------|----------------|-------------|
| Reference genome | GRCh38 / GRCm39 | Filename or FASTA header |
| Gene annotation | GENCODE v44 / Ensembl 110 | GTF file header or download source |
| SILVA (16S) | 138.1 | Filename: silva_138.1_SSURef |
| GTDB (metagenome) | r220 | Download directory name |
| UniProt | 2024_01 | Download date / release notes |
| GO | 2024-01-17 | OBO file header |
| KEGG | Release 109.0 | API or download date |
| MSigDB | v2023.2.Hs | `msigdbr` package version |

Record in checkpoint:
```yaml
databases:
  - name: "GRCh38"
    version: "GENCODE v44"
    source: "/ref/gencode/GRCh38.primary_assembly.genome.fa"
  - name: "SILVA"
    version: "138.1"
    source: "/db/silva/silva_138.1_SSURef_NR99.fasta"
```
</IRON-LAW>

## 4. Command Logging

<IRON-LAW>
Every command executed MUST be logged to the phase checkpoint file.

### Rules:
1. **Complete commands**: Full command line with all parameters (no "ran STAR with default settings")
2. **Input/output paths**: Absolute or project-relative paths
3. **Resource usage**: For HPC jobs, record SLURM job ID, walltime, memory used
4. **Exit codes**: Record whether command succeeded or failed
5. **Sequence**: Commands in execution order

### Checkpoint Format:
```yaml
commands:
  - step: 1
    description: "Quality trimming"
    command: |
      fastp -i data/raw/sample1_R1.fq.gz -I data/raw/sample1_R2.fq.gz \
        -o data/clean/sample1_R1.fq.gz -O data/clean/sample1_R2.fq.gz \
        --qualified_quality_phred 20 --length_required 50 \
        --thread 16 --html results/qc/sample1_fastp.html
    exit_code: 0
    slurm_job_id: "12345678"
    walltime: "00:15:32"
    peak_memory: "4.2 GB"
```
</IRON-LAW>

## 5. Random Seed Locking

<IRON-LAW>
ALL stochastic operations MUST use fixed seeds.

```python
# Python
import random, numpy as np
random.seed(42)
np.random.seed(42)

# Scanpy / scikit-learn
sc.pp.neighbors(adata, random_state=42)
sc.tl.umap(adata, random_state=42)
sc.tl.leiden(adata, random_state=42)
```

```r
# R
set.seed(42)
# Seurat
RunUMAP(obj, seed.use = 42)
FindClusters(obj, random.seed = 42)
```

Record seed value in checkpoint:
```yaml
random_seed: 42
```
</IRON-LAW>

## 6. Parameter Lock Protocol

<IRON-LAW>
Parameters locked in `project-anchor.yaml` → `analysis.locked_parameters` CANNOT be changed by the Agent without explicit user approval.

### Lock Timing:
- **Phase 0**: Initial parameters from Pre-Phase
- **Phase 2 (Analysis Design)**: Core parameters locked after design approval
- **Post Gate 2**: All analysis parameters frozen

### Modification Request:
If analysis requires parameter change:
1. Present reason with evidence
2. Show impact assessment
3. Get explicit user approval
4. Log change in `project-anchor.yaml → modification_log`

Self-modifying locked parameters → **Gate FAIL**.
</IRON-LAW>

## 7. Anti Cherry-Picking Rules

<IRON-LAW>
| Rule | Requirement |
|------|-------------|
| **Report ALL results** | Including non-significant, failed steps, and negative findings |
| **No selective reporting** | If you ran 10 comparisons, report all 10 — not just the 3 significant ones |
| **Outlier transparency** | If samples removed, state which and why; show results with AND without |
| **Failed steps** | Record in checkpoint; explain what was tried and why it failed |
| **Threshold pre-registration** | Significance cutoffs defined in Phase 2, not changed after seeing results |

### Report Template for Non-Significant Results:
```
We tested [comparison] using [test] and found no significant difference
(p = 0.23, padj = 0.45, Cohen's d = 0.12). This suggests [interpretation].
```

Hiding non-significant results → Gate CONDITIONAL at minimum.
</IRON-LAW>

## 8. Claim-Evidence Alignment

<IRON-LAW>
Every conclusion in the report MUST map to specific data evidence:

| Claim | Required Evidence |
|-------|------------------|
| "Gene X is differentially expressed" | DESeq2 result: padj, log₂FC, figure reference |
| "Samples cluster by treatment" | UMAP/PCoA figure, PERMANOVA R² and p-value |
| "Pathway Y is enriched" | enrichGO/GSEA result: padj, NES, gene count |
| "QC is acceptable" | QC grade with metrics table |

Format: **Claim → Evidence (Figure/Table/Data reference)**

Unsupported claims → Gate CONDITIONAL.
</IRON-LAW>

## 9. Result Verification Protocol

Before claiming any result:
1. **Check output files exist**: `ls -la output_file`
2. **Check files are non-empty**: `wc -l output_file` or `stat output_file`
3. **Spot-check content**: `head output_file` — does it look correct?
4. **Verify expected format**: Column count, header, data types

```bash
# Verification script template
echo "=== Result Verification ==="
for f in results/*.csv; do
  echo "$f: $(wc -l < $f) lines, $(head -1 $f | awk -F',' '{print NF}') columns"
done
```

Claiming results without verification → Self-check FAIL.

## 10. Red Flags — STOP

- Running analysis without recording tool versions
- Modifying locked parameters without user approval
- Reporting only significant results
- Unseeded stochastic operations
- Manual data manipulation (copy-paste, Excel edits)
- Commands not logged in checkpoint
- Results claimed without file verification

## 11. The Bottom Line

```
Unreproducible analysis is not analysis.
Log everything. Version everything. Report everything.
If it's not in the checkpoint, it didn't happen.
```
