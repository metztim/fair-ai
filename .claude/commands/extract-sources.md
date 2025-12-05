# Extract and archive sources from conversation

Scan the current conversation for URLs and add them to the investigation's sources.yaml.

## Instructions

### 1. Identify the current investigation

Look for context clues:
- Recent file reads/edits in `research/investigations/*/`
- Ask user if unclear which investigation to update

### 2. Extract URLs from conversation

Scan the conversation for:
- URLs in WebFetch tool calls
- URLs in WebSearch results
- URLs mentioned in user messages
- URLs in file contents that were read

### 3. Deduplicate against existing sources

Read the current `sources.yaml` and skip any URLs already present.

### 4. For each new URL, gather metadata

Create a source entry with:

```yaml
- id: "{domain}-{topic}-{date}"
  title: "[Extract from page title or context]"
  url: "{full URL}"
  type: "[article|report|academic|government-data|social-media|reference|tool]"
  author: "[Extract if available]"
  accessed: "{YYYY-MM-DD}"
  reliability: "[very-high|high|medium|low]"
  archive:
    wayback: null
    wayback_date: null
  key_claims:
    - "[Main claim relevant to investigation]"
  tags: ["relevant", "tags"]
```

### 5. Reliability scoring guide

- **very-high**: Government data (BLS, SEC), peer-reviewed academic, primary regulatory filings
- **high**: Major research firms (McKinsey, BCG), reputable news (NYT, WSJ), company press releases
- **medium**: Tech analysis sites, Wikipedia, industry blogs
- **low**: Social media, unverified claims, opinion pieces

### 6. Archive to Wayback Machine

For each new source URL:

1. Submit to Wayback Machine: `https://web.archive.org/save/{url}`
2. Wait for confirmation
3. Update the source entry with:
   - `wayback`: The archive URL
   - `wayback_date`: Date of archive

Note: Rate limit to 1 request per 5 seconds to avoid blocking.

### 7. Update sources.yaml

- Add new sources to the `sources:` list
- Update `metadata.total_sources` count
- Update `metadata.archived_count` for successfully archived sources
- Update `metadata.last_updated` date

### 8. Git commit

```
research({slug}): add {N} sources from session

- {N} new sources extracted
- {M} archived to Wayback Machine
```

### 9. Report to user

Output summary:
- Number of URLs found in conversation
- Number that were already in sources.yaml
- Number of new sources added
- Number successfully archived
- Any archiving failures
