---
description: Submit a computational task to the Slurm cluster — auto-generates job script from task description, validates resources, submits via sbatch, and monitors status
---

Submit a computation task to the HPC cluster via Slurm.

## Instructions

1. Load the `slurm-execution` skill
2. **Read `hpc-env.yaml`** from the project root
   - If it doesn't exist, ask the user for cluster info and create one
3. Ask the user (if not already specified):
   - What task to run? (script path, pipeline step, or description)
   - Which partition? (base / gpu / fat) — suggest based on task type
   - Resource requirements? — use `hpc-env.yaml` defaults if not specified
4. **Generate** a Slurm job script in `scripts/slurm/`
5. **Pre-submission checklist**:
   - Script has execute permission (`chmod 750`)
   - Log directory exists (`mkdir -p logs/slurm`)
   - Input files exist
   - Partition has available nodes (`sinfo -p {partition}`)
6. **Submit** with `sbatch` and capture job ID
7. **Report** job ID and expected wait time
8. Show how to monitor: `squeue -j {JOB_ID}`

## Quick Examples

User: "帮我提交一个 fastp 质控任务"
→ Generate QC job script → submit to base partition → report job ID

User: "提交 DADA2 降噪到 fat 节点"
→ Generate DADA2 job script → submit to fat partition → report job ID

User: "帮我查看作业状态"
→ Run `squeue -u $(whoami)` and `sacct` → report status

## Important

- Always read `hpc-env.yaml` for cluster-specific settings — never hardcode paths
- Use `--dependency=afterok` when the task depends on a previous step
- Verify outputs after job completion — "finished" ≠ "succeeded"
