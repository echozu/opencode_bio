---
name: pipeline-execution
description: Use when G2 (pipeline freeze) gate has passed — orchestrates all pipeline execution including QC, profiling, and downstream analysis for the appropriate data type; manages G3 gate and iteration
---

<HARD-GATE>
Do NOT begin full-scale pipeline execution without passing G3. Exploratory runs on a subset are permitted before G3.
</HARD-GATE>

# Pipeline Execution (Phase 4)

## Overview

This skill orchestrates all pipeline execution. It operates in TWO stages:

- **Phase 4a (Exploratory)**: Run the core pipeline on a subset of samples to validate the approach before committing to full-scale execution.
- **Phase 4b (Full Execution)**: Complete, rigorous execution of the pipeline on all samples.

## G3 Gate Checklist — Execution Readiness

Before entering Phase 4a, verify ALL items:

- [ ] analysis-protocol.yaml locked (G2 passed)
- [ ] All tools installed with correct versions
- [ ] All databases downloaded with correct versions
- [ ] Input data files complete and verified
- [ ] Host DNA removal completed (for shotgun data)
- [ ] Sufficient compute resources available (RAM, disk, CPU/GPU)
- [ ] Output directory structure created
- [ ] Environment/conda files prepared for reproducibility
- [ ] Backup of raw data verified

### HPC/Slurm Additional Checks

If `project-anchor.yaml` → `resources.compute` contains "HPC" or "cluster", or if `hpc-env.yaml` exists in the project root, ALSO verify:

- [ ] `hpc-env.yaml` exists and is configured for this cluster
- [ ] Slurm is accessible (`sinfo` returns partition info)
- [ ] Target partition has available nodes
- [ ] `scripts/slurm/` directory created for job scripts
- [ ] `logs/slurm/` directory created for job logs
- [ ] Storage paths in `hpc-env.yaml` are accessible

If HPC is detected, load the `slurm-execution` skill and use Slurm `sbatch` for all heavy computation steps instead of running directly. Refer to the `slurm-execution` skill's Decision Matrix for what counts as "heavy."

If ANY item fails, STOP and resolve before proceeding.

## Phase 4a — Exploratory Stage

<IRON-LAW>
Phase 4a is NOT optional. Before running the full pipeline, validate on a SUBSET:
- For amplicon: run 3-5 representative samples through full pipeline
- For shotgun: run 2-3 samples through full pipeline
- Check outputs at each step for quality and sanity

This catches parameter errors and pipeline bugs BEFORE processing all samples.
</IRON-LAW>

### Phase 4a Execution Steps

1. **Select representative subset** — include one sample from each group, covering depth range
2. **Run QC pipeline** on subset → verify QC statistics
3. **Run primary analysis** (denoising/assembly/profiling) on subset → verify outputs
4. **Run one downstream analysis** (e.g., diversity) on subset → verify results
5. **Domain sanity check** — do results make biological sense?

**Output:** `docs/04_execution/phase4a-exploration-report.md`

```
Phase 4a Exploration Report:
════════════════════════════
Samples tested: [list]

QC results:
  Reads before QC: [range]
  Reads after QC: [range]
  Host DNA removed: [%]

Primary analysis results:
  [Type A] ASVs detected: [N], taxonomy assigned: [%]
  [Type M] Assembly N50: [value], MAGs: [N]
  [Type R] Species detected: [N], mapping rate: [%]

Downstream preview:
  [Brief diversity or differential results]

Domain sanity: [PASS / ISSUES — describe]
Pipeline issues: [list or "none"]
```

### ⛔ Phase 4a Decision Point (MANDATORY STOP)

<IRON-LAW>
After Phase 4a, present the exploration report and STOP. The user decides what to do next.
</IRON-LAW>

```
Phase 4a exploration complete. Report above.

MY ASSESSMENT: [summarize findings]

YOUR OPTIONS:
1. ✅ PROCEED — Pipeline validated. Run full-scale on all [N] samples.
2. 🔧 ADJUST — Modify specific parameters based on findings:
   [list proposed changes]
3. 🔄 RETURN TO PHASE 3 — Pipeline design needs fundamental change.
4. ↩️ RETURN TO PHASE 2 — Analysis design needs reconsideration.

Which option?
```

## Phase 4b — Full Execution

### Execution Order

Based on data type, invoke the appropriate analysis sub-skill:

| Data Type | Primary Sub-Skill | Then |
|-----------|------------------|------|
| A (Amplicon) | `amplicon-analysis` | `downstream-analysis` |
| M (Assembly) | `metagenome-assembly` | `downstream-analysis` + `functional-annotation` |
| R (Read-Based) | `metagenome-readbased` | `downstream-analysis` + `functional-annotation` |
| C (Combined) | Both A + (M or R) | `downstream-analysis` + cross-validation |

### Execution Discipline

For every pipeline step:

1. **Log the exact command** — tool, version, parameters, input, output
2. **Check exit codes** — non-zero exit = investigate before continuing
3. **Verify outputs** — expected files exist and have reasonable size
4. **Run domain sanity check** — results make biological sense
5. **Record in pipeline log** — `docs/04_execution/pipeline-log.md`

**On HPC clusters (when `slurm-execution` skill is loaded):**
- Write each step as a Slurm job script in `scripts/slurm/`
- Submit via `sbatch` and record job ID in pipeline log
- Use `--dependency=afterok` to chain dependent steps
- Verify job success with `sacct` before proceeding to the next step
- Log Slurm job ID, runtime, and resource usage in pipeline log

### Post-Execution Reviews

After primary analysis is complete, dispatch sub-agent reviews:

**QC Reviewer** (use `qc-reviewer-prompt.md`):
- Verify QC metrics meet thresholds across ALL samples
- Flag any samples that should be excluded
- Confirm no systematic quality issues

**Pipeline Completeness Reviewer** (use `pipeline-completeness-prompt.md`):
- Verify all planned analyses were executed
- Check all output files exist
- Verify parameter compliance with locked protocol
- Check reproducibility (commands logged, versions recorded)

### Iteration Within Phase 4

<IRON-LAW>
If downstream analysis reveals issues, DO NOT silently fix them:
1. Document the issue in pipeline-log.md
2. Present to user with options (adjust, re-run, accept with caveat)
3. Get user approval before re-running with changed parameters
4. Log ALL parameter changes in analysis-protocol.yaml change_log

"Quick fix" without documentation = irreproducible science.
</IRON-LAW>

**After 3 consecutive failures** (same analysis step failing repeatedly):
- Trigger `pivot-or-kill` skill
- Present options: fix, pivot to different approach, or skip with documentation

## Domain Sanity Check — Full Results

Before declaring Phase 4 complete:

- [ ] Taxonomic profiles dominated by expected gut organisms
- [ ] Diversity metrics within expected ranges for gut microbiome
- [ ] Group differences (if any) are biologically plausible
- [ ] No evidence of batch effects or technical artifacts
- [ ] Negative controls (if present) show minimal contamination
- [ ] Results consistent across biological replicates within groups
- [ ] Functional annotations are biologically plausible

<IRON-LAW>
## ⛔ MANDATORY STOP — After Phase 4 Completion

When all analyses are done, **END YOUR RESPONSE** with a results summary:

```
Phase 4 complete. Results summary:
  - Samples processed: [N/N]
  - Key taxonomic findings: [summary]
  - Diversity results: [summary]
  - Differential abundance: [N features significant]
  - Functional findings: [summary]
  - Figures generated: [N]
  - Issues encountered: [list or "none"]

Shall I proceed to Phase 5 (Results Integration)?
This will include a multi-agent discussion panel to stress-test
the findings before report writing.
```

Do NOT invoke `results-integration` or begin organizing results in the same response.
Do NOT skip to report writing.

**STOP. WAIT. The user must reply before you proceed.**
</IRON-LAW>

## Red Flags — STOP

- Running full pipeline without Phase 4a exploration
- Ignoring failed pipeline steps
- Not logging exact commands
- Changing parameters without documentation and user approval
- Proceeding with samples that failed QC
- Not running domain sanity check on results

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Phase 4a is overkill for a standard pipeline" | Phase 4a catches parameter errors cheaply. Full re-run is expensive. |
| "The error was minor, I fixed it" | Minor fixes without documentation = irreproducible. Log everything. |
| "All samples should be included" | Failed QC samples corrupt results. Exclude and document. |
| "The domain sanity check is just common sense" | Common sense fails when you're deep in data. Systematically check. |
| "I'll log the commands later" | Later = never. Log NOW, at execution time. |
| "Re-running is wasteful" | Running on bad parameters is MORE wasteful. Fix first, then re-run. |
