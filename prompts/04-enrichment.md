# Stage 4: Per-person enrichment

Input: `people/people.csv` rows with `enrichment_status = pending`. Claim a row by setting it to `in_progress` first.

Per person, capture into `notes` (structured, pipe-separated) and set `enrichment_status = enriched`:

1. LinkedIn: current title confirmed, tenure, 2 to 3 most recent posts or activity themes.
2. Event cross-reference: do they appear on any Luma guest list in `events/*/speakers.csv`? If yes, add that event slug to their `events` column; meeting them in person beats cold outreach.
3. Company context: the company's named AI initiative or internal AI program (press, engineering blog, job postings). This feeds the outreach question wording.
4. Email: Apollo match, then validate. `email_status`: verified | guessed | none.

Runs in parallel across agents (Hyperagent, Claude Code). The status column is the lock.
