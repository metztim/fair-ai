# Save research session and commit changes

Create a session log, update the investigation, and commit all changes.

## Instructions

### 1. Identify the current investigation

Look for context clues:
- Recent file reads/edits in `research/investigations/*/`
- Ask user if unclear which investigation to update

### 2. Create session log

Create a new file in `sessions/` with naming convention: `{YYYYMMDD}-{brief-description}.md`

Use this template:

```markdown
# Session Log: {YYYY-MM-DD} - {Brief Description}

**Duration:** ~X hours/minutes
**Type:** [{research}|{analysis}|{writing}|{review}]

---

## Session Objectives

- [What was the goal of this session?]

---

## Key Questions Explored

[List the main questions investigated]

---

## Key Findings

### Finding 1: [Title]
[Description with supporting evidence]

### Finding 2: [Title]
[Description]

---

## Sources Consulted

See `sources.yaml` for full list. Key sources this session:
- [List main sources used]

---

## Open Questions for Future Sessions

1. [Questions that emerged]

---

## Next Actions

- [ ] [Specific next steps]

---

## Files Created/Modified This Session

- [List files changed]
```

### 3. Update INVESTIGATION.md

- Add any new key findings to the "Key Findings" section
- Update "Open Questions" with new questions discovered
- Add any new methodology insights
- Update "Last Updated" date in header

### 4. Run source extraction

Execute the logic from `/extract-sources`:
- Scan conversation for URLs
- Add new sources to sources.yaml
- Archive to Wayback Machine (if enabled)

### 5. Git operations

1. Stage all changed files in the investigation directory
2. Commit with message:

```
research({slug}): session {YYYYMMDD} - {brief description}

- Session log: {session filename}
- {N} new sources added
- Key findings: [brief summary]
```

### 6. Report to user

Output:
- Session log path
- Changes made to INVESTIGATION.md
- Number of sources added
- Commit hash
- Reminder: "Run `git push` to sync to remote"

### 7. Optional: Ask about next session

Prompt user:
> "Would you like to schedule the next research session? If so, what topics should we explore?"

Store answer in session log's "Next Actions" section.
