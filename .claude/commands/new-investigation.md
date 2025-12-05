# Create a new research investigation

Initialize a new investigation in the ai-watchdog research framework.

## Instructions

When the user runs `/new-investigation [topic]`, create a complete investigation structure:

### 1. Parse the topic
Extract the topic from the command argument. Create a URL-friendly slug (lowercase, hyphens, no special characters).

### 2. Create directory structure

```
research/investigations/{slug}/
├── INVESTIGATION.md     # Main investigation document
├── sources.yaml         # Source tracking file
├── sessions/            # Session logs directory
├── drafts/              # Article drafts directory
└── research/            # Supporting research files
```

### 3. Initialize INVESTIGATION.md

Use this template:

```markdown
# {Topic} Investigation

**Status:** Active
**Started:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}
**Lead:** Tim Metz

---

## Hypothesis

[State the main hypothesis or research question]

---

## Key Findings

*No findings yet - investigation in progress*

---

## Methodology

### Data Sources
- [To be determined]

### Approach
1. [To be determined]

See `sources.yaml` for complete source list.

---

## Open Questions

1. [Initial questions to explore]

---

## Related Files

- `sources.yaml` - All sources with archive links
- `sessions/` - Session logs from research conversations
- `drafts/` - Article drafts
- `research/` - Supporting research documents
```

### 4. Initialize sources.yaml

```yaml
metadata:
  investigation: "{slug}"
  created: "{YYYY-MM-DD}"
  last_updated: "{YYYY-MM-DD}"
  total_sources: 0
  archived_count: 0

sources: []
```

### 5. Create initial session log

Create `sessions/{YYYYMMDD}-initial.md` with:

```markdown
# Session Log: {YYYY-MM-DD} - Investigation Setup

**Duration:** ~X minutes
**Type:** [setup]

---

## Session Objectives

- Initialize investigation structure
- Define initial hypothesis
- Identify first research directions

---

## Initial Hypothesis

[Copy from INVESTIGATION.md]

---

## Next Actions

- [ ] Define methodology
- [ ] Identify key sources
- [ ] Begin initial research
```

### 6. Git operations

1. Create a new branch: `research/{slug}`
2. Stage all new files
3. Commit with message: `research({slug}): initialize investigation`
4. Report the branch name and file paths to user

### 7. Output to user

Confirm creation with:
- Branch name
- Directory path
- Files created
- Next steps (suggest `/save-research-session` after initial research)
