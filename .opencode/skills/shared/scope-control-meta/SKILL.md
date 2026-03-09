---
name: scope-control-meta
description: "META-CONTROL — triggers when scope expansion detected, repeated failures occur, or data quality issues threaten analysis validity. Forces structured decision: continue / pivot / downgrade / halt."
---

# Scope Control & Pivot-or-Kill — Meta-Control for Omics Analysis

## Overview

This skill combines scope control and failure escalation into a single meta-control layer. It triggers when the analysis drifts beyond its original design, when repeated failures occur, or when data quality threatens validity.

**Core principles:**
- Focus is a feature. Scope creep is a bug.
- Repeated failure is signal, not noise. Escalate, don't iterate blindly.
- The Agent proposes; the User decides.

## 1. Trigger Conditions

Any ONE of these activates this skill:

### Scope Expansion Triggers:
- User requests additional analysis type beyond initial design
- Analysis plan grows to cover > 3 distinct analysis branches
- New comparison groups or conditions added mid-analysis
- Cross-omics integration requested (requires orchestrator)
- "One more analysis" appears more than twice

### Failure Triggers:
- 3 consecutive pipeline failures on the same step
- 3 consecutive reviewer REVISE verdicts at any Gate
- Tool/database consistently produces unexpected results
- QC grade D or F on majority of samples

### Data Quality Triggers:
- Data quality insufficient for planned analysis but user insists
- Batch effects dominate biological signal after correction
- Sample sizes too small for planned statistical tests
- Key metadata missing for planned comparisons

## 2. Scope Expansion Protocol

When scope expansion is detected:

### Step 1: WARN
```
"⚠️ Scope expansion detected: [describe what was added].
Current analysis plan already includes [N] analysis branches.
Adding [new request] would expand the scope by ~[X]%."
```

### Step 2: QUANTIFY
```
Current scope:
  - Analysis branches: N (was M at Phase 0)
  - Estimated compute time: X hours
  - Estimated additional phases: Y

Proposed addition:
  - New analysis: [description]
  - Additional compute: +Z hours
  - Additional skills/tools needed: [list]
  - Impact on timeline: [estimate]
```

### Step 3: PROPOSE
Present prioritized options:
```
a) ADD to current analysis (scope +X%)
   Risk: Dilutes focus, extends timeline by ~Y
   
b) REPLACE — swap with lower-priority existing analysis
   What to defer: [specific analysis to move to "future work"]
   
c) DEFER to separate analysis session
   Record in project-anchor.yaml → future_work
   
d) REJECT — current scope is sufficient
```

### Step 4: PRESENT — User Decides
```
THE AGENT CANNOT DECIDE SCOPE CHANGES.
Present options. Stop. Wait for user decision.
```

After user decides → update `project-anchor.yaml` and `session-state.yaml`.

## 3. Pivot-or-Kill Protocol (Failure Escalation)

### The Iron Law

```
AFTER 3 CONSECUTIVE FAILURES AT THE SAME STEP, STOP. ESCALATE TO USER.
```

No fourth attempt. No "quick fix." Escalate.

### Step 1: Summarize Status Honestly
State plainly:
- What was tried (each of the 3 attempts)
- What failed (specific errors, metrics, gaps)
- Trend direction (improving, flat, worsening)

Do NOT soften language. "All three attempts failed" is correct. "Results showed variability" is evasion.

### Step 2: Classify Root Cause

| Category | Signal | Example |
|----------|--------|---------|
| **Tool/env issue** | Same error across attempts | Missing dependency, version conflict |
| **Data quality** | Consistent poor metrics | Too few reads, high contamination |
| **Method mismatch** | Tool not appropriate for data type | Using bulk methods on scRNA data |
| **Parameter issue** | Results improve with parameter changes | Threshold too strict/lenient |
| **Fundamental** | No approach works | Insufficient biological signal |

### Step 3: Present Exactly Four Options

**a) FIX** — Address root cause and retry
- Specify: what changes (tool, parameter, approach)
- Estimated additional time
- Likelihood of success

**b) PIVOT** — Change analysis approach
- Specify: new method/tool to use
- What stays, what changes
- Risk assessment

**c) DOWNGRADE** — Reduce analysis scope
- Specify: what analyses to drop
- What can still be concluded from available results
- Impact on final report

**d) HALT** — Stop this analysis branch
- Archive all results and logs
- Document what was attempted
- Record in checkpoint as "halted — [reason]"

### Step 4: User Decides
```
THE AGENT CANNOT MAKE THIS DECISION. WAIT FOR USER.
```

Present options. Do not nudge. Do not recommend. User decides.

## 4. Data Quality Escalation

When data quality threatens analysis validity:

```
⚠️ DATA QUALITY CONCERN
═══════════════════════════════════════════════

Issue: [specific problem]
Impact: [which analyses are affected]
Current grade: [D/F or specific metric failure]

Evidence:
  - [metric 1]: [value] (threshold: [threshold])
  - [metric 2]: [value] (threshold: [threshold])

Options:
  a) PROCEED with limitations documented
     → Results will carry caveat: "[specific limitation]"
     → Some downstream analyses may not be valid
     
  b) ADJUST analysis plan
     → Drop: [analyses requiring higher quality data]
     → Keep: [analyses robust to this quality level]
     
  c) HALT and recommend re-sequencing
     → Estimated cost/time for new data: [if known]
     
Your decision?
```

## 5. Integration with Execution Modes

| Mode | Scope expansion | Failure (3x) | Data quality |
|------|:---------------:|:------------:|:------------:|
| **interactive** | Stop + present options | Stop + present options | Stop + present options |
| **semi-auto** | Stop + present options | Stop + present options | Stop + present options |
| **auto** | Stop + present options | Stop + present options | Stop + present options |

**All modes stop for meta-control decisions.** These are not automatable — they require human judgment about scientific direction.

## 6. Logging Requirements

All meta-control events MUST be logged:

```yaml
# In checkpoint file
meta_control_events:
  - type: "scope_expansion"
    trigger: "User requested additional differential analysis"
    decision: "defer"
    timestamp: "YYYY-MM-DD HH:MM"
    details: "Added to future_work in project-anchor.yaml"
    
  - type: "failure_escalation"  
    trigger: "3 consecutive STAR alignment failures"
    root_cause: "tool_env_issue"
    decision: "fix"
    details: "Resolved by updating STAR index for correct genome version"
```

## 7. Red Flags — STOP

- Attempting a 4th fix without user consultation
- Downplaying failure severity ("almost working", "close")
- Silently expanding scope without flagging
- Proceeding with grade F data without user acknowledgment
- Blaming infrastructure to avoid confronting method issues
- Lowering success criteria instead of escalating

## 8. Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "One more try might work" | You said that twice. Escalate. |
| "We can fit all analyses in" | Scope creep dilutes quality. Focus. |
| "The data quality is fine for exploratory work" | If quality is D/F, say so. User decides risk. |
| "I'll just add this quick analysis" | Nothing is quick. Quantify impact first. |
| "Killing the analysis is too drastic" | Stopping saves resources for valid analyses. |
| "The user will be disappointed" | Honest reporting > false optimism. Always. |

## The Bottom Line

```
Scope drifting → quantify → present options → user decides
3 failures → stop → summarize → escalate → user decides
Bad data → report honestly → present options → user decides

The Agent proposes. The User decides. Always.
```
