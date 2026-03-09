---
name: results-review
description: >
  Use after Phase 4 (Results & Visualization) is complete — performs Gate 3 Type A blind review
  of scRNA-seq results. Dispatches a blind reviewer with NO conversation context, only structured
  artifacts. Checks annotation consistency, claim-evidence alignment, figure quality, and
  anti-cherry-pick compliance. MANDATORY before advancing to Phase 5.
---

# Results Review — Gate 3 (Type A Blind Review)

## Overview

Gate 3 is a **Type A (Blind Review)** gate. The reviewer receives ONLY structured artifacts — NO conversation history, NO prior context. This ensures objectivity: the reviewer evaluates what was produced, not what was intended.

<IRON-LAW>
The blind reviewer MUST NOT receive:
- Conversation history
- User's stated expectations
- Previous phase discussions
- Any context that could bias the review

The reviewer receives ONLY:
- Cluster summary with cell counts and proportions
- Marker gene lists per cluster
- DE results with statistics
- Figures (descriptions or file paths)
- QC metrics summary

This is the ENTIRE point of Type A review: unbiased, evidence-only assessment.
</IRON-LAW>

## Step 1 — Prepare Structured Artifacts

Before dispatching the blind reviewer, compile these artifacts:

### Required Artifacts
```
ARTIFACT PACKAGE FOR BLIND REVIEW:
══════════════════════════════════

1. CLUSTER SUMMARY:
   | Cluster | Cell Count | % Total | Assigned Type | Confidence |
   |---------|-----------|---------|---------------|------------|
   [for each cluster]

2. TOP MARKER GENES PER CLUSTER:
   | Cluster | Gene | avg_log2FC | pct.1 | pct.2 | p_val_adj |
   [top 10 markers per cluster]

3. DIFFERENTIAL EXPRESSION RESULTS:
   | Comparison | Up-regulated | Down-regulated | Method | Correction |
   [for each comparison]

4. QC METRICS SUMMARY:
   - Total cells: [N]
   - Cells after filtering: [N] ([%] retained)
   - Median genes/cell: [N]
   - Clusters: [N]
   - Samples: [N]
   - Integration method: [method]

5. FIGURE INVENTORY:
   | Figure | Type | Description |
   [list all generated figures]

6. NEGATIVE RESULTS:
   [list any failed analyses, non-significant comparisons, excluded samples]
```

## Step 2 — Dispatch Blind Reviewer

Use the `blind-reviewer-prompt.md` template in this skill's directory.

<IRON-LAW>
Dispatch via Task tool with ONLY the artifact package above.
Do NOT include any explanatory text, rationale, or conversation context.
The reviewer must form their own judgment from evidence alone.
</IRON-LAW>

## Step 3 — Process Review Verdict

| Verdict | Action |
|---------|--------|
| **PASS** | Proceed to Phase 5 (Advanced Analysis) |
| **CONDITIONAL** | Address specific issues, re-submit artifacts, re-review (max 2 rounds) |
| **FAIL** | Return to Phase 3 or Phase 4 to fix fundamental issues |

### On CONDITIONAL verdict:
1. Document each issue raised
2. Fix the specific issues (do NOT re-do entire analysis)
3. Update the artifact package with fixes
4. Re-dispatch blind reviewer with updated artifacts
5. If still CONDITIONAL after 2 rounds → escalate to user

### On FAIL verdict:
```
⚠️ GATE 3 FAILURE — Blind Review
═══════════════════════════════════

The blind reviewer has identified fundamental issues:

[List issues with severity]

YOUR OPTIONS:
1. 🔄 RETURN TO PHASE 3 — Re-run core analysis with corrections
2. 🔧 FIX SPECIFIC ISSUES — Address reviewer concerns and re-submit
3. ⏸️ PAUSE — Consult with domain experts before proceeding

Which option do you prefer?
```

## Step 4 — Document Gate 3 Results

Save to `docs/scrna/gates/gate-3-results-review.yaml`:
```yaml
gate: 3
type: "Type A — Blind Review"
reviewer_verdict: [PASS/CONDITIONAL/FAIL]
rounds: [N]
issues_raised: [list]
issues_resolved: [list]
artifacts_reviewed: [list]
timestamp: [ISO 8601]
```

<IRON-LAW>
## ⛔ MANDATORY STOP

After Gate 3 resolution, present the verdict summary and STOP.

"Gate 3 blind review complete. Verdict: [X]. Proceed to Phase 5 (Advanced Analysis)?"
"Gate 3 盲审完成。结论：[X]。是否进入第5阶段（高级分析）？"

Then STOP.
</IRON-LAW>
