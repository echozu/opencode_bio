---
name: parameter-lock
description: Use when analysis parameters, databases, or thresholds have been confirmed in analysis-protocol.yaml — enforces immutability of locked analysis components without explicit user authorization
---

# Parameter Lock (Discipline Layer)

## Overview

Changing analysis parameters after confirmation is not optimization — it is goalpost-moving. This skill activates after G2 (pipeline freeze) and remains in effect until project end.

**Core principle:** Locked means locked. No silent modifications.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

<IRON-LAW>
ANALYSIS PARAMETERS, ONCE CONFIRMED IN analysis-protocol.yaml, ARE IMMUTABLE WITHOUT USER PERMISSION.
</IRON-LAW>

## What Is Locked

After G2 pipeline freeze, the following are immutable:

- **QC parameters** (quality threshold, min length, adapter handling)
- **Denoising parameters** (truncation lengths, max expected errors, chimera method)
- **Taxonomy classifier and database version** (SILVA version, confidence threshold)
- **Assembly parameters** (assembler, min contig length)
- **Profiling tool and database versions** (MetaPhlAn version, database release)
- **Rarefaction depth**
- **Differential abundance tool and thresholds** (significance, LFC, correction method)
- **Network analysis parameters** (correlation method, prevalence filter)
- **Random seeds** (where applicable)
- **Visualization standards** (color palette, figure format)

## What Is Allowed

- Additional downstream analyses may be **added** (e.g., adding a network analysis not originally planned)
- Additional figures may be generated
- Exploratory analyses that do NOT replace locked primary analyses

Added analyses **cannot replace** locked primary analyses and **cannot** be used to override primary analysis conclusions.

## Change Request Process

```
IF you believe a locked parameter must change:

1. EXPLAIN: What exactly needs to change?
2. JUSTIFY: Why is the current value flawed?
3. PROVE: Show evidence the locked value is defective (not just suboptimal)
4. WAIT: User decides — not you
5. LOG: Record old value, new value, reason in change_log

Skip any step = unauthorized modification = results invalidation
```

## Red Flags — STOP

- Quietly changing QC thresholds after seeing initial results
- Switching taxonomy database version mid-analysis
- Adjusting rarefaction depth after seeing diversity results
- Using a different significance threshold than specified
- Changing differential abundance tool after seeing results from the locked tool
- "Forgetting" a locked parameter and using a different value

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This parameter isn't quite right" | You argued for it in Phase 3. To change, go through the change request process. |
| "A different threshold shows better results" | That's exactly why changing is forbidden. |
| "The database was updated" | If true, justify the switch to user. Don't change silently. |
| "Just trying an alternative analysis" | Adding supplementary is fine. Replacing primary is not. |
| "It's a minor adjustment" | Minor adjustments to locked items require user approval. Always. |
| "Standard practice changed" | Convince the user. Don't change silently. |
| "The rarefaction depth is too low" | Then it should have been caught in Phase 3. Request change formally. |

## The Bottom Line

```
Locked parameter + no user approval = do not touch
```

Unauthorized modification of analysis parameters invalidates all downstream results. No exceptions.
