---
name: report-review
description: >
  Use after Phase 6 (Report Generation) is complete — performs Gate 4 Type B deliberation review.
  Dispatches 2 reviewers (Methods Reviewer + Interpretation Reviewer) via Task tool for multi-round
  deliberation on the final report. Both must PASS for Gate 4 to clear. MANDATORY before finalizing.
---

# Report Review — Gate 4 (Type B Deliberation)

## Overview

Gate 4 is a **Type B (Deliberation)** gate. Two specialist reviewers independently evaluate the final report through controlled multi-round deliberation. Both reviewers must PASS for the gate to clear.

<IRON-LAW>
Gate 4 is NOT optional. Every scRNA-seq analysis report must pass this gate before being delivered to the user as "final." A report that skips Gate 4 is an unreviewed draft, not a finished product.
</IRON-LAW>

## Reviewer Composition

| Agent | Template | Focus |
|-------|----------|-------|
| **Methods Reviewer** | `methods-reviewer-prompt.md` | Reproducibility, completeness, technical accuracy |
| **Interpretation Reviewer** | `interpretation-reviewer-prompt.md` | Biological plausibility, claim-evidence alignment, honest framing |

For per-section polishing (optional, recommended for publication-targeted reports), also dispatch:
| **Adversarial Reviewer** | `adversarial-reviewer-prompt.md` | Claim over-reach, missing caveats, reviewer #2 attack |

## Step 1 — Prepare Review Package

Compile the following for reviewers:

```
REPORT REVIEW PACKAGE:
══════════════════════

1. FULL REPORT: [docs/scrna/checkpoints/phase-6-report.yaml or report file]

2. ANALYSIS PROTOCOL SUMMARY:
   - Normalization: [method]
   - Integration: [method]
   - Clustering: [method, resolution]
   - DE method: [method]
   - Tool versions: [list]

3. CLAIM-EVIDENCE MAP:
   | Claim | Evidence | Figure/Table | Statistical Support |
   [from Phase 4/5 outputs]

4. FIGURE INVENTORY:
   [list all figures with descriptions]

5. NEGATIVE RESULTS:
   [documented negative/non-significant results]
```

## Step 2 — Dispatch Reviewers (Parallel)

Use the prompt templates in this skill's directory:
- `methods-reviewer-prompt.md` for Methods Reviewer
- `interpretation-reviewer-prompt.md` for Interpretation Reviewer

**REQUIRED SUB-SKILL:** Follow `multi-round-deliberation` protocol.

## Step 3 — Multi-Round Deliberation (max 2 rounds)

After each round:
1. **Collect** verdicts from both reviewers
2. **Synthesize** feedback and identify required changes
3. **Revise** the report based on feedback
4. **Re-dispatch** both reviewers with revised report
5. Check convergence: both PASS → done; any FAIL → next round

**Convergence:** Both reviewers PASS → Gate 4 PASS
**Non-convergence after 2 rounds:** Escalate to user

## Step 4 — Per-Section Polishing (Optional)

For reports targeting peer-reviewed publication, apply per-section polishing with 3 agents:
- Methods Reviewer (reproducibility)
- Interpretation Reviewer (biological accuracy)
- Adversarial Reviewer (Reviewer #2 attack)

Present EACH SECTION individually and wait for user feedback.

## Step 5 — Document Gate 4 Results

Save to `docs/scrna/gates/gate-4-final-review.yaml`:
```yaml
gate: 4
type: "Type B — Deliberation"
methods_reviewer_verdict: [PASS/CONDITIONAL/FAIL]
interpretation_reviewer_verdict: [PASS/CONDITIONAL/FAIL]
rounds: [N]
issues_raised: [list]
issues_resolved: [list]
timestamp: [ISO 8601]
```

<IRON-LAW>
## ⛔ MANDATORY STOP

After Gate 4 resolution, present the final verdict and STOP.

"Gate 4 report review complete. Both reviewers: [X]. Report is finalized."
"Gate 4 报告审查完成。两位审稿人：[X]。报告已定稿。"

Then STOP.
</IRON-LAW>
