---
name: multi-round-deliberation
description: Reusable protocol for multi-agent discussions that iterate until convergence. Used by data-assessment (Phase 1), analysis-design-validation (Phase 2), pipeline-design (Phase 3), results-integration (Phase 5), and report-generation (Phase 6).
---

# Multi-Round Deliberation Protocol

## Overview

A single round of feedback is NOT a discussion. Real deliberation requires iteration: agents identify issues → main agent fixes them → agents verify the fix → repeat until resolved.

## The Problem with Single-Round Feedback

```
WRONG (anti-pattern):
  3 agents give opinions → main agent "synthesizes" → done
  → Issues may be noted but never actually resolved

RIGHT (this protocol):
  3 agents give opinions → main agent modifies artifact →
  agents re-check → if unresolved, modify again →
  repeat until convergence or max rounds
```

## Core Protocol

### Shared Value Framework

All agents in a deliberation share these values, injected into every prompt:

```
SHARED VALUES (inject into every agent prompt):
═══════════════════════════════════════════════
Target standard: [from project-anchor.yaml — venue or quality target]
Analysis type: [A/M/R/C from project-anchor.yaml]
Value proposition: [from project-anchor.yaml]

OPTIMIZATION TARGET: "Would this survive peer review at [target venue]?"

SCORING RUBRIC:
  - PASS: No fatal or major issues. Ready to proceed.
  - CONDITIONAL: Major issues exist but are addressable. Needs another round.
  - FAIL: Fatal issues. Fundamental rethinking needed.

CONVERGENCE RULE: Deliberation ends when ALL agents score PASS,
or when max rounds are reached and remaining issues are presented to user.

ANTI-DIVERGENCE: If you disagree with another agent's feedback,
state specifically WHY and propose a CONCRETE alternative.
"I disagree" without a counter-proposal is not constructive.
═══════════════════════════════════════════════
```

### Deliberation Loop

```
┌─────────────────────────────────────────────────────┐
│  ROUND N                                            │
│                                                     │
│  1. ASSESS (parallel)                               │
│     Dispatch ALL agents with current artifact        │
│     Each returns: issues + verdict (PASS/COND/FAIL) │
│                                                     │
│  2. CHECK CONVERGENCE                               │
│     All PASS? → END (consensus reached)             │
│     Any FAIL or COND + round < max? → go to step 3  │
│     Max rounds reached? → END (present to user)     │
│                                                     │
│  3. MODIFY                                          │
│     Main agent incorporates feedback:                │
│     - Fix all issues marked as addressable           │
│     - For disagreements: choose the stronger argument│
│     - Update the artifact                            │
│                                                     │
│  4. FULL RE-ASSESS (next round)                     │
│     Dispatch ALL agents again with:                  │
│     - The complete modified artifact                 │
│     - Summary of changes made since last round       │
│     - Previous round's issues for reference          │
│     All agents review the full artifact              │
│                                                     │
│  → Back to step 2                                   │
└─────────────────────────────────────────────────────┘
```

### Round Limits (non-negotiable)

| Context | Max Rounds | Rationale |
|---------|-----------|-----------|
| Phase 1 data assessment | 5 | Data quality determines everything downstream |
| Phase 2 analysis design | 5 | Analysis design is the project's foundation |
| Phase 3 pipeline design | 5 | Locked parameters affect all results |
| Phase 5 story design | 5 | The story determines the report's quality |
| Phase 6 per-section polishing | 5 | Each section must be thoroughly vetted |
| Phase 6 full-report review | 5 | Full-report coherence is critical |

### Convergence Criteria

Deliberation ends (consensus) when ALL of:
- No agent gives verdict "FAIL"
- No remaining issues tagged "fatal" or "critical"
- All agents explicitly state their concerns from previous rounds are addressed

### Non-Convergence Handling

If max rounds reached and agents still disagree:

```
DELIBERATION SUMMARY (presented to user):
══════════════════════════════════════════

Rounds completed: N / max N
Final verdicts: Agent A: [PASS/COND/FAIL], Agent B: [...], Agent C: [...]

RESOLVED issues (N):
  ✅ [issue] — addressed in round [N] by [change]

UNRESOLVED issues (N):
  ⚠️ [issue] — Agent [X] says: "[position]"
              — Agent [Y] says: "[counter-position]"
              — My recommendation: [your judgment]

DECISION NEEDED from you:
  1. [Option A — side with Agent X]
  2. [Option B — side with Agent Y]
  3. [Option C — compromise proposal]
  4. Run one more round of discussion
```

### Re-Assessment Template (Round 2+)

```
Call Task tool with:
  description: "[agent role] — round [N] review"
  prompt: |
    [SHARED VALUES block]

    This is round [N] of deliberation.
    YOUR previous concerns:
    [paste this agent's issues from last round]

    OTHER agents' concerns (for context):
    [paste summary of other agents' issues]

    Changes made since last round:
    [paste summary of what changed and why]

    COMPLETE MODIFIED ARTIFACT:
    [paste the full updated artifact]

    Review the COMPLETE artifact (not just the changes):
    1. For EACH of your previous concerns: RESOLVED / PARTIALLY / NOT ADDRESSED
    2. Any NEW issues introduced by the modifications?
    3. Any issues with how OTHER agents' concerns were addressed?
    4. Overall verdict: PASS / CONDITIONAL / FAIL

    If CONDITIONAL or FAIL: state exactly what remains to be fixed.
  subagent_type: "generalPurpose"
```

### Agent Disagreements

When agents directly contradict each other:

1. **Present both positions** with their reasoning
2. **Evaluate evidence**: which position is better supported?
3. **Choose the stronger argument** for the modification
4. **In re-assessment**: tell the overruled agent what you chose and why
5. **If persistent disagreement after 2 rounds**: present to user as a strategic choice

### Anti-Patterns to Avoid

| Anti-pattern | Why it's wrong | What to do instead |
|-------------|---------------|-------------------|
| Accepting "CONDITIONAL" without specifics | "Conditional" means there ARE remaining issues | Ask the agent to specify exactly what remains |
| Running max rounds mechanically | Wastes time if consensus reached early | Check convergence after every round; stop early if PASS |
| Ignoring minority opinion | Minority may be right | Address the concern or explain why it's overruled |
| "Synthesizing" by averaging opinions | Synthesis is not averaging | Choose the strongest argument for each issue |
| Skipping agents in later rounds | Fixes can introduce new issues | Dispatch ALL agents every round |

## Red Flags — STOP

- Only dispatching 1 or 2 agents instead of 3
- Not re-dispatching ALL agents after modifications
- Declaring convergence when CONDITIONAL verdicts exist
- Ignoring an agent's persistent FAIL
- Not presenting non-convergence to user

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Two agents agree, so skip the third" | The third may catch what the other two missed. |
| "Round 1 was sufficient" | Check convergence — if all PASS, great. If not, iterate. |
| "The CONDITIONAL is minor" | Minor issues compound. Address them. |
| "Re-assessment is wasteful" | Modifications can introduce new issues. Full re-assessment is necessary. |
| "The agents are repeating themselves" | If they repeat concerns, the concerns weren't addressed. Fix them. |
