---
description: Force update session-state.yaml with current analysis progress (跨Agent进度同步)
---

You MUST perform the following steps in EXACT order. Do NOT skip any step.

## Step 1 — Read current session-state.yaml

```bash
cat session-state.yaml 2>/dev/null || echo "FILE_NOT_FOUND"
```

If the file does not exist, create it using the session-state template format.

## Step 2 — Determine current analysis state

Based on the conversation history, determine:
- Which agent are you? (metagenome-expert / scrna-expert / transcriptome-expert / other)
- What phase are you in? (0-6)
- What phases have been completed?
- What are the key output files produced so far?
- What are the key findings so far?
- Any warnings or issues?
- Data quality grade (A/B/C/D/F)?

## Step 3 — Update session-state.yaml

Update ONLY your agent's section. The required fields are:

```yaml
agents:
  {your-agent-name}:
    status: "in_progress"           # not_started | in_progress | completed | failed | paused
    current_phase: N                # 0-6
    data_quality_grade: "X"         # A/B/C/D/F or null
    completed_phases: [0, 1, ...]   # list of completed phase numbers
    key_outputs:
      - path: "path/to/output"
        description: "what this file contains"
    key_findings:
      - "finding 1"
      - "finding 2"
    warnings:
      - "any issues or concerns"
    anchor_file: "path/to/project-anchor.yaml"
```

Also update:
- `last_updated`: current timestamp
- `last_agent`: your agent name

## Step 4 — Read back and confirm

Read the file back to verify your update was written correctly:

```bash
cat session-state.yaml
```

Confirm that your section was updated correctly.

## Step 5 — Report summary

Tell the user:
- What was updated
- Current phase and status
- Key findings so far
- Any cross-agent information from other agents' sections
