---
name: slurm-execution
description: |
  CRITICAL INFRASTRUCTURE — MUST load when hpc-env.yaml exists in project
  root OR sbatch/squeue/sinfo commands are detected. Routes bioinformatics
  computation (fastp, STAR, bowtie2, MEGAHIT, DADA2, Kraken2, MetaPhlAn,
  DESeq2, Seurat, Scanpy) to Slurm compute nodes. Prevents heavy tasks
  from running on login nodes (which would be killed by admins and harm
  other users). Load during Phase 0 environment detection, enforce from
  Phase 4 onward. Required for ALL omics analysis on HPC clusters.
allowed-tools: [Read, Write, Edit, Bash]
---

<HARD-GATE>
Before using this skill, verify:
1. The system is an HPC cluster with Slurm installed (`which sbatch` succeeds)
2. `hpc-env.yaml` exists in the project root (or create one interactively)
3. The user's storage paths are confirmed
</HARD-GATE>

# HPC Slurm Execution Skill

## Overview

This skill teaches you how to properly execute computational tasks on a Slurm-managed HPC cluster. The core principle is simple:

**Lightweight tasks → execute directly on the login node.**
**Heavy computation → write a Slurm script → submit with `sbatch`.**

## When to Load This Skill

Load `slurm-execution` when ANY of these are true:
- `project-anchor.yaml` has `resources.compute` containing "HPC" or "cluster" or "Slurm"
- The `hpc-env.yaml` config file exists in the project root
- The user mentions they're on a shared cluster or HPC environment
- You detect Slurm commands are available (`sinfo`, `sbatch`, `squeue`)

## Decision Matrix: Direct vs Slurm

<IRON-LAW>
NEVER run heavy computation directly on a login node. Login nodes are shared — hogging resources blocks other users and may get your process killed by admins.
</IRON-LAW>

| Task Type | Execute Where | Method |
|-----------|---------------|--------|
| File I/O (read, write, edit, copy, mv) | Login node | Direct `bash` |
| Git operations | Login node | Direct `bash` |
| Package installation (`pip`, `conda`, `bun install`) | Login node | Direct `bash` |
| Small scripts (<30s, <2GB RAM) | Login node | Direct `bash` |
| Viewing results, parsing logs | Login node | Direct `bash` |
| `squeue`, `sinfo`, `sacct` monitoring | Login node | Direct `bash` |
| QC pipeline (fastp, FastQC, MultiQC) | **Compute node** | `sbatch` |
| Sequence alignment (STAR, bowtie2, BWA) | **Compute node** | `sbatch` |
| Assembly (MEGAHIT, metaSPAdes) | **Compute node** | `sbatch` |
| Denoising (DADA2, QIIME2) | **Compute node** | `sbatch` |
| Taxonomy (MetaPhlAn, Kraken2) | **Compute node** | `sbatch` |
| R/Python data analysis (>2GB data) | **Compute node** | `sbatch` |
| Deep learning / GPU tasks | **GPU node** | `sbatch -p gpu` |
| Large memory tasks (>64GB) | **Fat node** | `sbatch -p fat` |

**Rule of thumb:** If the task touches raw sequencing data, runs a bioinformatics tool, or processes >1GB of data, use Slurm.

## Step 0: Environment Detection

When this skill is first loaded, run these checks:

```bash
# 1. Verify Slurm is available
which sbatch && echo "SLURM_AVAILABLE=true" || echo "SLURM_AVAILABLE=false"

# 2. Check current node type
hostname
# Login nodes typically named: login01, login02, mgmt*, etc.

# 3. Check available partitions
sinfo --format="%P %a %l %D %T %N" --noheader

# 4. Check user's storage paths
echo "HOME=$HOME"
ls /jinxianstor/home/$(whoami) 2>/dev/null && echo "JINXIAN_OK=true"
ls /zaixianstor/home/$(whoami) 2>/dev/null && echo "ZAIXIAN_OK=true"

# 5. Check if hpc-env.yaml exists
cat hpc-env.yaml 2>/dev/null || echo "NO_HPC_ENV_YAML"
```

If `hpc-env.yaml` does not exist, create one interactively (see Config section below).

## Step 1: The `hpc-env.yaml` Config

This file lives in the **project root** and stores cluster-specific settings. Create it once, use everywhere.

```yaml
# hpc-env.yaml — HPC Cluster Configuration
# This file is the single source of truth for cluster-specific settings.
# Edit this file ONCE when setting up the project on a new cluster.

cluster:
  name: "BioHPC"                       # Cluster display name
  scheduler: "slurm"                   # Job scheduler type
  login_node: "login01"               # Current login node hostname

storage:
  home: "/jinxianstor/home/<USERNAME>"  # Primary home (large, slower)
  fast: "/zaixianstor/home/<USERNAME>"  # Fast storage (smaller, SSD/NVMe)
  project: "/jinxianstor/home/<USERNAME>/openBio"  # Project root on cluster
  scratch: "/zaixianstor/home/<USERNAME>/scratch"   # Scratch space for temp files

partitions:
  default: "base"
  available:
    base:
      description: "General compute nodes"
      nodes: 19
      cpus_per_node: 192        # 2×AMD 9654 (96 cores each)
      mem_per_node_gb: 768
      max_walltime: "168:00:00" # 7 days
      gpu: false
    gpu:
      description: "GPU compute nodes"
      nodes: 2
      cpus_per_node: 192
      mem_per_node_gb: 1024
      max_walltime: "168:00:00"
      gpu: true
      gpu_type: "NVIDIA L20 48GB"
      gpus_per_node: 8
    fat:
      description: "High-memory nodes"
      nodes: 3
      cpus_per_node: 176        # 4×Intel 8444h (44 cores each)
      mem_per_node_gb: 4096
      max_walltime: "168:00:00"
      gpu: false

environment:
  conda_init: "source /jinxianstor/apps/Anaconda3/conda.env"
  bun_init: |
    export BUN_INSTALL="$HOME/.bun"
    export PATH="$BUN_INSTALL/bin:$PATH"
  # Add custom module loads or env setup here:
  # module_loads: ["module load gcc/12.2", "module load cuda/12.0"]
  custom_init: ""

defaults:
  # Default resources for common task types
  qc:
    partition: "base"
    cpus: 8
    mem_gb: 16
    time: "4:00:00"
  alignment:
    partition: "base"
    cpus: 16
    mem_gb: 64
    time: "12:00:00"
  assembly:
    partition: "base"
    cpus: 32
    mem_gb: 128
    time: "24:00:00"
  taxonomy:
    partition: "base"
    cpus: 16
    mem_gb: 64
    time: "8:00:00"
  diversity_analysis:
    partition: "base"
    cpus: 8
    mem_gb: 32
    time: "4:00:00"
  deep_learning:
    partition: "gpu"
    cpus: 16
    mem_gb: 64
    time: "48:00:00"
    gpus: 1
  large_memory:
    partition: "fat"
    cpus: 32
    mem_gb: 256
    time: "24:00:00"

notifications:
  # Slurm email notifications (optional)
  email: ""
  events: "END,FAIL"  # NONE, BEGIN, END, FAIL, ALL
```

<IRON-LAW>
If `hpc-env.yaml` does not exist when this skill is loaded:
1. Ask the user for their username and cluster details
2. Generate the config with sensible defaults
3. Write it to the project root
4. Ask the user to review and confirm

NEVER hardcode paths or partition names — always read from `hpc-env.yaml`.
</IRON-LAW>

## Step 2: Writing Slurm Job Scripts

### Script Naming Convention

All Slurm job scripts go in `scripts/slurm/` with the naming pattern:

```
scripts/slurm/{step_number}_{task_name}.job
```

Example: `scripts/slurm/01_qc_fastp.job`, `scripts/slurm/02_denoise_dada2.job`

### Job Script Template

Every Slurm job script MUST follow this template:

```bash
#!/bin/bash
#==============================================================================
# Job: {DESCRIPTIVE_NAME}
# Project: {PROJECT_NAME}
# Generated by: OpenCode Bio Metagenome Expert
# Date: {YYYY-MM-DD}
#==============================================================================

#SBATCH --job-name={short_name}
#SBATCH --partition={partition}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --mem={mem}G
#SBATCH --time={walltime}
#SBATCH --output={project_path}/logs/slurm/%x_%j.log
#SBATCH --error={project_path}/logs/slurm/%x_%j.err
#{OPTIONAL: --gres=gpu:N}
#{OPTIONAL: --mail-user=email}
#{OPTIONAL: --mail-type=END,FAIL}

# ============ Environment Setup ============
{conda_init}
{custom_init}

# Activate project-specific conda env (if applicable)
# conda activate {env_name}

# ============ Verification ============
echo "========================================="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Start: $(date)"
echo "Working dir: $(pwd)"
echo "CPUs: $SLURM_CPUS_PER_TASK"
echo "Memory: $SLURM_MEM_PER_NODE MB"
echo "========================================="

# Verify tools are available
{tool_verification_commands}

# ============ Main Task ============
cd {working_directory}

{MAIN_COMMANDS}

# ============ Post-Task ============
EXIT_CODE=$?
echo "========================================="
echo "Exit code: $EXIT_CODE"
echo "End: $(date)"
echo "========================================="

# Write a completion marker file for the monitor to detect
if [ $EXIT_CODE -eq 0 ]; then
    echo "COMPLETED $(date)" > {project_path}/logs/slurm/.done_{step_name}
else
    echo "FAILED $(date) exit=$EXIT_CODE" > {project_path}/logs/slurm/.failed_{step_name}
fi

exit $EXIT_CODE
```

### GPU Job Template Addition

For GPU jobs, add these lines:

```bash
#SBATCH --gres=gpu:{num_gpus}

# In the verification section:
nvidia-smi
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
```

## Step 3: Submitting Jobs

### Pre-submission Checklist

Before every `sbatch`, verify:

```bash
# 1. Script has execute permission
chmod 750 scripts/slurm/{script}.job

# 2. Log directory exists
mkdir -p {project_path}/logs/slurm

# 3. Output directories exist
mkdir -p {output_dirs}

# 4. Input files exist and are readable
ls -la {input_files}

# 5. Partition has available resources
sinfo -p {partition} --format="%P %a %D %C" --noheader
```

### Submit and Record

```bash
# Submit and capture job ID
JOB_ID=$(sbatch scripts/slurm/{script}.job | awk '{print $4}')
echo "Submitted job $JOB_ID: {description}"

# Record in pipeline log
echo "$(date) | Step {N} | Job $JOB_ID | {description} | SUBMITTED" >> docs/04_execution/pipeline-log.md
```

### Job Dependencies (Pipeline Chains)

When steps depend on each other, use Slurm dependencies:

```bash
# Step 1: QC
JOB_QC=$(sbatch scripts/slurm/01_qc.job | awk '{print $4}')

# Step 2: Depends on QC completing successfully
JOB_DENOISE=$(sbatch --dependency=afterok:$JOB_QC scripts/slurm/02_denoise.job | awk '{print $4}')

# Step 3: Depends on denoising
JOB_TAXONOMY=$(sbatch --dependency=afterok:$JOB_DENOISE scripts/slurm/03_taxonomy.job | awk '{print $4}')

echo "Pipeline submitted: QC($JOB_QC) → Denoise($JOB_DENOISE) → Taxonomy($JOB_TAXONOMY)"
```

<IRON-LAW>
ALWAYS use `--dependency=afterok:$PREV_JOB` for pipeline steps that depend on previous outputs.
`afterok` means only run if the dependency SUCCEEDED (exit code 0).
If a step fails, downstream jobs won't run — this prevents cascading errors on bad data.
</IRON-LAW>

## Step 4: Monitoring Jobs

### Active Monitoring

```bash
# Check all user's jobs
squeue -u $(whoami) --format="%.10i %.20j %.10P %.8T %.12M %.12l %.6D %.4C %R"

# Check specific job
squeue -j {JOB_ID} -l

# Watch job status (run periodically)
squeue -u $(whoami) --format="%.10i %.20j %.10T" --noheader
```

### Interpreting Job States

| State | Meaning | Action |
|-------|---------|--------|
| `PENDING (PD)` | Waiting for resources | Wait, check with `squeue --start -j {ID}` for estimated start |
| `RUNNING (R)` | Currently executing | Monitor logs: `tail -f logs/slurm/{name}_{id}.log` |
| `COMPLETING (CG)` | Finishing up | Wait briefly |
| `COMPLETED (CD)` | Done successfully | Check outputs |
| `FAILED (F)` | Non-zero exit | Check error log: `cat logs/slurm/{name}_{id}.err` |
| `TIMEOUT (TO)` | Exceeded time limit | Increase `--time` or optimize script |
| `CANCELLED (CA)` | User/admin cancelled | Check reason |
| `OUT_OF_MEMORY (OOM)` | Exceeded memory | Increase `--mem` or optimize memory usage |

### Result Collection

After a job completes:

```bash
# 1. Check exit status
sacct -j {JOB_ID} --format=JobID,State,ExitCode,Elapsed,MaxRSS,MaxVMSize --noheader

# 2. Check completion marker
cat {project_path}/logs/slurm/.done_{step_name} 2>/dev/null && echo "SUCCESS" || echo "CHECK ERRORS"

# 3. Verify output files exist and have reasonable size
ls -lh {expected_output_files}

# 4. Quick sanity check on outputs
head -20 {output_file}
wc -l {output_file}

# 5. Record in pipeline log
sacct -j {JOB_ID} --format=Elapsed,MaxRSS --noheader | head -1 | \
  xargs -I{} echo "$(date) | Step {N} | Job {JOB_ID} | COMPLETED | Runtime: {} " >> docs/04_execution/pipeline-log.md
```

<IRON-LAW>
NEVER assume a job succeeded without checking:
1. Exit code (via `sacct`)
2. Output files exist with non-zero size
3. Completion marker file exists
4. Log file shows no errors

"Job finished" ≠ "Job succeeded". Always verify.
</IRON-LAW>

## Step 5: Handling Failures

### Diagnosis Workflow

```bash
# 1. Get job details
sacct -j {JOB_ID} --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS,MaxVMSize,NodeList

# 2. Read error log
cat logs/slurm/{name}_{id}.err

# 3. Read last 50 lines of output log
tail -50 logs/slurm/{name}_{id}.log

# 4. Common fixes:
# OOM → increase --mem
# TIMEOUT → increase --time
# Exit code 1 → check tool error in stderr
# Exit code 127 → tool not found, check conda env
# Exit code 137 → killed by system (OOM or admin), increase resources
```

### Resubmission

```bash
# Fix the issue in the script, then resubmit
sbatch scripts/slurm/{script}.job

# For the same step with more resources:
sbatch --mem=128G --time=24:00:00 scripts/slurm/{script}.job
```

## Integration with Pipeline Execution

When the `pipeline-execution` skill is active and HPC resources are detected:

### Modified G3 Gate Checklist

In addition to the standard G3 checks, verify:
- [ ] `hpc-env.yaml` exists and is valid
- [ ] Slurm is accessible (`sinfo` works)
- [ ] Target partition has available nodes (`sinfo -p {partition}`)
- [ ] Log directory created: `mkdir -p {project}/logs/slurm`
- [ ] Slurm script directory created: `mkdir -p {project}/scripts/slurm`
- [ ] Storage space sufficient on target path (`df -h {path}`)

### Modified Execution Flow

Instead of running pipeline commands directly:

1. **Write** each pipeline step as a standalone Slurm job script in `scripts/slurm/`
2. **Verify** the script (check paths, tools, parameters)
3. **Submit** with `sbatch` and capture the job ID
4. **Monitor** — poll `squeue` until job completes or fails
5. **Verify** outputs after completion
6. **Log** results to `docs/04_execution/pipeline-log.md`
7. **Proceed** to next step only after successful verification

### Monitoring Polling Strategy

```bash
# Poll every 30 seconds until job completes
while squeue -j $JOB_ID --noheader 2>/dev/null | grep -q "$JOB_ID"; do
    echo "$(date): Job $JOB_ID still running..."
    sleep 30
done
echo "Job $JOB_ID finished. Checking status..."
sacct -j $JOB_ID --format=State --noheader | head -1
```

**In practice**, rather than blocking with a polling loop, you should:
1. Submit the job
2. Tell the user: "Job {ID} submitted to {partition}. Estimated wait: {time}."
3. Periodically check status when the user asks or when moving to next step
4. Use `--dependency=afterok` for automatic chaining

## Storage Strategy

| Content | Where to Store | Why |
|---------|---------------|-----|
| Raw data (FASTQ) | `/jinxianstor/home/<user>/` | Large files, long-term |
| Project code | `/jinxianstor/home/<user>/openBio/` | Persistent |
| Pipeline scripts | `/jinxianstor/home/<user>/{project}/scripts/` | Persistent |
| Intermediate files (BAM, temp) | `/zaixianstor/home/<user>/scratch/` | Fast I/O, temp |
| Final results | `/jinxianstor/home/<user>/{project}/results/` | Long-term |
| Logs | `/jinxianstor/home/<user>/{project}/logs/` | Persistent |

<IRON-LAW>
Heavy I/O operations (alignment, assembly) should write to fast storage (`/zaixianstor/`).
Final results should be copied back to persistent storage (`/jinxianstor/`).
Always clean up scratch space after pipeline completion.
</IRON-LAW>

## Full Pipeline Submission Example

Here is a complete example of submitting a 16S amplicon pipeline:

```bash
# Ensure directories exist
mkdir -p scripts/slurm logs/slurm

# Step 1: QC
JOB_QC=$(sbatch scripts/slurm/01_qc_fastp.job | awk '{print $4}')
echo "QC job: $JOB_QC"

# Step 2: DADA2 denoising (after QC)
JOB_DADA2=$(sbatch --dependency=afterok:$JOB_QC scripts/slurm/02_denoise_dada2.job | awk '{print $4}')
echo "DADA2 job: $JOB_DADA2"

# Step 3: Taxonomy assignment (after denoising)
JOB_TAX=$(sbatch --dependency=afterok:$JOB_DADA2 scripts/slurm/03_taxonomy.job | awk '{print $4}')
echo "Taxonomy job: $JOB_TAX"

# Step 4: Diversity analysis (after taxonomy)
JOB_DIV=$(sbatch --dependency=afterok:$JOB_TAX scripts/slurm/04_diversity.job | awk '{print $4}')
echo "Diversity job: $JOB_DIV"

# Step 5: Differential abundance (after taxonomy)
JOB_DIFF=$(sbatch --dependency=afterok:$JOB_TAX scripts/slurm/05_differential.job | awk '{print $4}')
echo "Differential job: $JOB_DIFF"

# Monitor all jobs
echo ""
echo "Pipeline submitted:"
echo "  QC($JOB_QC) → DADA2($JOB_DADA2) → Taxonomy($JOB_TAX)"
echo "                                        ├→ Diversity($JOB_DIV)"
echo "                                        └→ Differential($JOB_DIFF)"
echo ""
squeue -u $(whoami)
```

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "It's a small job, I'll run it directly" | Check the decision matrix. If it touches raw data or runs a bio tool, use Slurm. |
| "I don't need to check the outputs" | ALWAYS verify. Silent failures corrupt entire analyses. |
| "I'll use the login node, it's faster to start" | Login node is shared. Heavy jobs get killed. Use Slurm. |
| "I'll request maximum resources just in case" | Over-requesting wastes cluster resources and increases queue time. Use `hpc-env.yaml` defaults. |
| "The job failed, let me resubmit immediately" | Diagnose FIRST. Resubmitting the same broken script wastes queue time. |
| "I'll clean up scratch later" | Later = never. Add cleanup to the job script. |

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Slurm adds complexity" | Slurm adds REPRODUCIBILITY. Every job is logged, timed, and resourced. |
| "Direct execution is faster for development" | Fast on login node → slow for everyone else. Use `srun --pty bash` for interactive dev. |
| "hpc-env.yaml is overkill" | One config file vs hardcoding paths everywhere. The config saves time. |
| "Job dependencies are hard to set up" | Three lines of bash vs debugging a half-finished pipeline. Dependencies save time. |
