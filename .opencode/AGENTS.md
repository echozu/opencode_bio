# OpenCode Bio — Global Agent Rules

These rules apply to **ALL** agents in the system. They are automatically injected into every agent's context.

## 1. Infrastructure Detection (ALL Agents — Phase 0)

<IRON-LAW>
Before starting any analysis, you MUST check the compute environment:

```bash
which sbatch 2>/dev/null && echo "HPC_DETECTED=true" || echo "HPC_DETECTED=false"
test -f hpc-env.yaml && echo "HPC_CONFIG=true" || echo "HPC_CONFIG=false"
```

- If `hpc-env.yaml` exists → read `slurm-execution` skill IMMEDIATELY
- If `sbatch` is available → read `slurm-execution` skill IMMEDIATELY
- From Phase 4 onward, ALL heavy computation MUST use sbatch on HPC clusters
- NEVER run bioinformatics tools (fastp, STAR, bowtie2, MEGAHIT, DADA2, Kraken2, MetaPhlAn, DESeq2, Seurat, Scanpy, etc.) directly on login nodes
</IRON-LAW>

## 2. Cross-Agent State — session-state.yaml

All analysis agents MUST manage the shared progress file:

- **Phase 0 start** → Read `session-state.yaml` (if it exists) to check other agents' progress
- **After each Phase** → Update `session-state.yaml` with your own progress, key outputs, and findings
- **Phase 5 (Results Integration)** → Read all other agents' findings for cross-validation
- Only update YOUR OWN agent section — never modify another agent's data
- `cross_validation` section is shared — any agent can append

## 3. Skill Priority

When multiple skills cover similar functionality, use this priority:

1. **Domain-specific skills** (`skills/{domain}/`) → highest priority, domain workflows
2. **Shared skills** (`skills/shared/`) → cross-domain frameworks and discipline
3. **Bio tool skills** (`skills/bio/`) → tool-level usage details
4. **Contrib skills** (`skills/contrib/`) → external contributions
5. **Amplify skills** (`skills/amplify/`) → research methodology framework

## 4. Mandatory Skill Classes

Skills fall into four trigger categories:

| Category | Trigger | Examples |
|----------|---------|----------|
| 🔴 **MANDATORY** | IRON-LAW in Agent prompt; Phase 0 auto-detect | `slurm-execution` (HPC detected), `prompt-optimizer` (new analysis request) |
| 🟠 **PHASE-BOUND** | Skill routing table marks `●` (must use) | `qc-grading-framework` (Phase 1), `figure` (Phase 4) |
| 🟡 **CONDITION-TRIGGERED** | Description specifies conditions | `enrichment-framework` (differential results exist), `cell-translation` (Ribo-seq data) |
| 🟢 **ON-DEMAND** | AI self-judgment | bio/ tool skills, `network-analysis` |

<EXTREMELY-IMPORTANT>
MANDATORY and PHASE-BOUND skills are NOT optional. You CANNOT skip them.
If a skill is marked ● in your routing table for the current phase, you MUST read and follow it.
</EXTREMELY-IMPORTANT>

## 5. Execution Modes — Three-Tier Automation

<IRON-LAW>
Read `docs/project-anchor.yaml` → `execution.mode` field to determine behavior.
If the file does not exist yet (Pre-Phase / Phase 0), default to `interactive`.

| Behavior | interactive | semi-auto | auto |
|----------|:----------:|:---------:|:----:|
| Phase 间自动推进 | ❌ | ✅ | ✅ |
| Gate 处停下等用户 | ✅ | ✅ | ❌ (仅 FAIL 停下) |
| 触发盲审 (Gate) | 用户决定 | ✅ 自动 | ✅ 自动 |
| Review PASS → 继续 | 用户确认 | ✅ 自动 | ✅ 自动 |
| Review REVISE → 回炉 | 用户确认 | ✅ 自动 (max 2次) | ✅ 自动 (max 3次) |
| Review ABORT → 停下 | ✅ | ✅ | ✅ |
| 回炉达上限 → 停下 | ✅ | ✅ | ✅ |
| 命令失败 → 停下 | ✅ | ✅ | ✅ |
</IRON-LAW>

## 6. One Phase Per Turn

<IRON-LAW>
**interactive mode**: Complete ONLY ONE PHASE per response. After completing a phase or reaching a gate:
1. Present deliverables and/or gate checklist
2. **END YOUR RESPONSE — STOP GENERATING**
3. Wait for user to reply with explicit approval
4. Only then proceed to the next phase

**semi-auto mode**: Auto-advance between phases, but STOP at every Gate and wait for user approval.

**auto mode**: Auto-advance through phases AND gates. Only STOP when:
- Gate verdict = FAIL (fundamental) or ABORT
- Retry limit reached (3 attempts)
- Command execution failure
- Analysis complete (Phase 6 done)
</IRON-LAW>

## 7. Pre-Phase: Prompt Optimization

When receiving a **new analysis request** (not a continuation), ALL agents MUST:

1. Load `prompt-optimizer` skill
2. Probe data paths — `ls`/`tree` the user-provided directory
3. Parse intent — identify omics type, sample count, groups, analysis goals
4. Cross-validate — file types vs user description (磁盘为真 principle)
5. Generate structured 「分析规格确认书」(Analysis Specification)
6. Wait for user confirmation (support up to 3 rounds of iteration)
7. After confirmation → proceed to Phase 0 with pre-filled information

<EXTREMELY-IMPORTANT>
Pre-Phase output feeds directly into Phase 0. Do NOT re-ask questions that were already confirmed in Pre-Phase.
</EXTREMELY-IMPORTANT>

## 8. File Checkpoint Protocol

<IRON-LAW>
Every Phase completion MUST write checkpoint files. This is NON-NEGOTIABLE — disk files survive context compaction, LLM memory does not.

### 8.1 Checkpoint Files
After completing Phase N, MUST write:
```
docs/{domain}/checkpoints/phase-{N}-{name}.yaml
```
Minimum fields: phase, name, status, timestamp, inputs, outputs, tools_used, next_phase

### 8.2 Gate Review Files
Gate conclusions MUST be persisted:
```
docs/{domain}/gates/gate-{N}-{type}-review.yaml
```
Fields: gate, type, review_type (blind/deliberation), verdict (PASS/CONDITIONAL/FAIL), issues, summary

### 8.3 session-state.yaml Update
After EVERY phase, update session-state.yaml (see §9 for protocol).

### 8.4 Verification
After writing any checkpoint/gate file:
1. **Write** the file
2. **Read** it back
3. **Confirm** content matches intent in your response

Failure to write checkpoint = Phase NOT complete. You MUST write before ending your response.
</IRON-LAW>

## 9. session-state.yaml — Write-Read-Confirm Protocol

When updating session-state.yaml, you MUST follow this three-step protocol:
1. **Write** the update using the Write/Edit tool
2. **Read** it back immediately using the Read tool
3. **Confirm** the content matches your intent in your response text

This prevents situations where you THINK you updated the file but didn't actually do it.

<EXTREMELY-IMPORTANT>
If you have NOT updated session-state.yaml after completing a Phase, you MUST do so
BEFORE ending your response. The Phase is NOT complete until session-state.yaml is updated.

Minimum fields to update each time:
- `agents.{your-domain}.status` → "in_progress" or "completed"
- `agents.{your-domain}.current_phase` → current phase number
- `agents.{your-domain}.completed_phases` → append the phase you just completed
- `agents.{your-domain}.key_outputs` → append any new output files
</EXTREMELY-IMPORTANT>

## 10. Discipline Rules (Core — All Agents)

<IRON-LAW>
These discipline rules are embedded in every agent. Detailed steps are in `reproducibility-discipline` skill.

| Rule | Requirement | Violation Consequence |
|------|-------------|----------------------|
| **Parameter Lock** | project-anchor.yaml locked params cannot be self-modified | Gate FAIL |
| **Anti Cherry-Pick** | Report ALL results including non-significant and failures | Gate CONDITIONAL |
| **Claim-Evidence Alignment** | Every conclusion maps to specific data/figure | Gate CONDITIONAL |
| **Reproducibility** | All commands, tool versions, DB versions logged to checkpoint | Self-check FAIL |
| **Result Verification** | Verify BEFORE claiming — output files exist and non-empty | Self-check FAIL |
| **Figure Quality** | Publication-grade: title, axis labels, legend, color scheme | Gate CONDITIONAL |

### Honesty Principle
- Command failure → report immediately, no retry without acknowledgment
- QC below threshold → report true grade, no sugar-coating
- Uncertain → say "uncertain", do not guess
- Bad results → report honestly, do not hide or minimize
</IRON-LAW>

## 11. Language Adaptation

Respond in the **same language** as the user's input:
- Chinese input → Chinese response
- English input → English response
- Technical terms (tool names, database names, file paths) stay in English regardless
