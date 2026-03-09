---
name: multi-round-deliberation
description: "Reusable protocol for multi-agent review discussions in omics analysis. Used by methods-reviewer and results-reviewer at Gate checkpoints. Ensures review issues are actually resolved through iterative deliberation."
---

# Multi-Round Deliberation Protocol — Omics Analysis

## Overview

A single round of feedback is NOT a review. Real deliberation requires iteration: reviewer agents identify issues → main agent fixes them → reviewers verify the fix → repeat until resolved. This protocol standardizes this loop across all Gate checkpoints in omics analysis.

## The Problem with Single-Round Feedback

```
WRONG (anti-pattern):
  Reviewer checks analysis → notes issues → main agent "acknowledges" → done
  → Issues may be noted but never actually resolved
  → No verification that fixes addressed the concerns

RIGHT (this protocol):
  Reviewer checks → main agent modifies → reviewer re-checks →
  if unresolved, modify again → repeat until convergence or max rounds
```

## Core Protocol

### Shared Context (injected into every reviewer prompt)

```
SHARED CONTEXT (inject into every reviewer in this deliberation):
═══════════════════════════════════════════════════════════════════
Analysis domain: [from project-anchor.yaml: data.type]
Current phase: [phase number]
Data quality grade: [from QC assessment]
Execution mode: [interactive/semi-auto/auto]

OPTIMIZATION TARGET: "Is this analysis scientifically sound, 
reproducible, and correctly interpreted?"

SCORING RUBRIC:
  - PASS: No critical issues. Ready to proceed to next phase.
  - CONDITIONAL: Issues exist but are addressable. Needs revision.
  - FAIL: Fundamental problems. Cannot proceed.

CONVERGENCE RULE: Deliberation ends when ALL reviewers score PASS,
or when max rounds reached and remaining issues are presented to user.

ANTI-DIVERGENCE: If you disagree with another reviewer, state 
specifically WHY and propose a CONCRETE alternative.
═══════════════════════════════════════════════════════════════════
```

### Deliberation Loop

```
┌─────────────────────────────────────────────────────┐
│  ROUND N                                            │
│                                                     │
│  1. ASSESS (parallel)                               │
│     Dispatch ALL reviewers with current artifact     │
│     Each returns: issues + verdict (PASS/COND/FAIL) │
│                                                     │
│  2. CHECK CONVERGENCE                               │
│     All PASS? → END (consensus reached)             │
│     Any FAIL/COND + round < max? → go to step 3    │
│     Max rounds reached? → END (present to user)     │
│                                                     │
│  3. MODIFY                                          │
│     Main agent incorporates feedback:               │
│     - Fix all issues marked as addressable          │
│     - For disagreements: choose stronger argument   │
│     - Update the artifact + checkpoint              │
│                                                     │
│  4. FULL RE-ASSESS (next round)                     │
│     Dispatch ALL reviewers with:                    │
│     - Complete modified artifact                    │
│     - Summary of changes since last round           │
│     - Previous round's issues for reference         │
│     → Back to step 2                                │
└─────────────────────────────────────────────────────┘
```

### Round Limits

| Gate | Reviewers | Max Rounds | Rationale |
|------|-----------|:----------:|-----------|
| **Gate 1** (QC) | QC Reviewer (Type A) | 3 | QC issues are usually clear-cut |
| **Gate 2** (Design) | Pipeline Reviewer (Type A) + Deliberation (Type B) | 3 | Design choices need focused review |
| **Gate 3** (Results) | Results Reviewer (Type A) | 3 | Statistical and interpretation review |
| **Gate 4** (Report) | All Reviewers (Type A) | 3 | Final quality assurance |

### Convergence Criteria

Deliberation ends (consensus) when ALL of:
- No reviewer gives verdict "FAIL"
- No remaining issues tagged "critical" or "fatal"
- All reviewers confirm previous concerns are addressed

### Non-Convergence Handling

If max rounds reached and reviewers still disagree:

```
DELIBERATION SUMMARY (presented to user):
══════════════════════════════════════════

Rounds completed: N / max N
Final verdicts: Reviewer A: [PASS/COND/FAIL], Reviewer B: [...]

RESOLVED issues (N):
  ✅ [issue] — addressed in round [N] by [change]

UNRESOLVED issues (N):
  ⚠️ [issue] — Reviewer [X]: "[position]"
              — Reviewer [Y]: "[counter-position]"
              — My recommendation: [your judgment]

DECISION NEEDED from you:
  1. [Option A — accept current state]
  2. [Option B — additional revision]
  3. [Option C — proceed with documented limitations]
  4. Run one more round of deliberation
```

## Re-Assessment Prompt Template (Round 2+)

```
Call Task tool with:
  description: "[reviewer role] — round [N] review"
  prompt: |
    [SHARED CONTEXT block]
    
    This is round [N] of deliberation. Previous round concerns:
    ===
    YOUR previous concerns:
    [paste this reviewer's issues from last round]
    
    OTHER reviewers' concerns (for context):
    [paste summary]
    ===
    
    Changes made since last round:
    ===
    [paste summary of modifications]
    ===
    
    COMPLETE MODIFIED ARTIFACT:
    [paste full updated analysis/results/report section]
    
    Review the COMPLETE artifact (not just changes). Answer:
    
    1. For EACH previous concern: RESOLVED / PARTIALLY / NOT ADDRESSED
    2. Any NEW issues introduced by modifications?
    3. Issues with how OTHER reviewers' concerns were addressed?
    4. Overall verdict: PASS / CONDITIONAL / FAIL
    
    If CONDITIONAL or FAIL: state exactly what remains to be fixed.
```

## Integration with Omics Analysis Gates

### Gate 1 — QC Assessment Review

```
Artifact: QC report + quality grade + preprocessing decisions
Reviewers: QC Reviewer (Type A — blind review)
Max rounds: 3
Focus: QC metrics accuracy, grade assignment, preprocessing appropriateness
Critical checks:
  - Grade matches actual metrics (no inflation)
  - Problematic samples identified
  - Preprocessing steps justified
```

### Gate 2 — Analysis Design Review

```
Artifact: Analysis plan + parameter choices + tool selection
Reviewers: Pipeline Reviewer (Type A) + optional Deliberation Agent (Type B)
Max rounds: 3
Focus: Method appropriateness, parameter validity, statistical plan soundness
Critical checks:
  - Tools appropriate for data type and study design
  - Statistical tests match data distribution and sample size
  - Parameters within accepted ranges for the field
```

### Gate 3 — Results Review

```
Artifact: Analysis results + figures + statistical outputs
Reviewers: Results Reviewer (Type A — blind review)
Max rounds: 3
Focus: Result validity, interpretation accuracy, claim-evidence alignment
Critical checks:
  - Statistical tests correctly applied and reported
  - Figures meet publication standards
  - Conclusions supported by data
  - Non-significant results reported
```

### Gate 4 — Final Report Review

```
Artifact: Complete analysis report
Reviewers: All available reviewers
Max rounds: 3
Focus: Completeness, accuracy, reproducibility documentation
Critical checks:
  - All phases represented
  - Methods section complete (tools + versions + params)
  - Figures referenced and described
  - Limitations discussed
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why | Fix |
|-------------|-----|-----|
| Accepting CONDITIONAL without asking what's needed | Issues remain unresolved | Ask reviewer to specify exactly what remains |
| Running max rounds when consensus reached in round 1 | Wastes tokens | Check convergence after every round; stop early |
| Ignoring minority reviewer opinion | May catch real issues | Address or explicitly explain why overruled |
| "Synthesizing" by averaging opinions | Not meaningful | Choose strongest argument per issue |
| Skipping reviewers in later rounds | Fixes can introduce new issues | Dispatch ALL reviewers every round |

## Execution Mode Behavior

| Mode | Round progression | User involvement |
|------|------------------|-----------------|
| **interactive** | Present each round's result; wait for user before next round | User approves each step |
| **semi-auto** | Auto-run rounds until convergence or max; present final summary | User reviews final outcome |
| **auto** | Auto-run all rounds; only stop if FAIL persists at max rounds | Minimal user involvement |
