# SF Events GTM Pipeline

A Ranch Lab pipeline that turns a list of San Francisco Bay Area events (November to December 2026) into an enriched, outreach ready list of ICP individuals: the people running enablement, onboarding, learning and development, and technical programs inside the companies speaking at, sponsoring, or exhibiting at those events.

The repo is built to be worked by both humans and agents. `CLAUDE.md` holds the operating instructions any agent reads on open. This README explains the whole process.

## The idea

Events are a wedge into companies, and speakers are a wedge into org charts. The pipeline cascades:

```
events  →  speakers & exhibitors  →  companies  →  ICP people  →  enrichment  →  outreach
```

Every stage writes structured files into this repo, so the state of the pipeline is always visible, diffable, and resumable by whoever (or whatever) picks it up next.

## The process, end to end

### Stage 0: Events as source of truth
30 events (24 confirmed, 6 watch list) were parsed into `events/events.csv`: conferences (AI Engineer Code Summit, QCon SF, Microsoft Ignite, Fortune Brainstorm AI), Luma meetups, and invite only dinners. Each event has a slug, date, URL, access model, and audience note.

### Stage 1: Speaker and attendee extraction
Different event types need different extraction methods:

* **Conferences with published rosters**: fetched directly. AI Engineer Code Summit publishes its full schedule as agent readable open data at `/code/2026/llms.txt`. QCon lists 135 confirmed speakers.
* **Luma meetups**: the public page shows hosts and featured speakers. The guest list (the real volume) only unlocks once registered, and gets swept with a logged in browser agent 2 to 3 days before each event.
* **Invite only events**: reconstructed from news coverage and LinkedIn posts, lower confidence, flagged as such.

Result so far: 190 speakers captured across the two big conferences, in `events/<slug>/speakers.csv`.

### Stage 2: Company rollup
All companies dedupe into `companies/companies.csv` (112 so far), ranked by how many people they have across how many events. Headcount gets verified with three sources in order, Apollo, then People Data Labs, then LinkedIn, and is only trusted when all three agree.

### Stage 3: ICP expansion
For each company, Apollo people search pulls the actual targets, three title buckets:

* **Enablement**: sales, revenue, field, and engineering enablement, L&D, learning experience
* **Onboarding**: customer onboarding, implementation, customer education and enablement
* **TPM**: technical program managers, program managers, program management leadership

Seniority filter: senior, manager, director, VP, head. Results:

* `people/people.csv`: the curated shortlist, 79 priority targets, hand filtered for internal facing roles and director+ titles
* `people/pool/pool.csv`: the entire pool, 2,456 unique people across 50 company domains, every row carrying its Apollo ID and the events its company is attending. Includes Apollo's fuzzy tail (adjacent titles like generic CSMs), filterable via the `icp_category` column and title text.

`tools/parse_apollo.py` parses raw Apollo search output into the pool, deduping by Apollo ID, so future pulls drop straight in.

### Stage 4: Enrichment (next up)
Apollo bulk match by ID unlocks full names, verified work emails, and LinkedIn URLs (1 credit per match). Then per person enrichment runs in parallel across agents: LinkedIn activity, the company's named internal AI initiative, and cross referencing against Luma guest lists, because "see you Thursday at the meetup" beats any cold email. Status columns in the CSVs are the locks that keep agents from double working a row.

### Stage 5: Outreach
Drafts follow the template and rules in `prompts/05-outreach.md`. The core rule: never open with a research fact. Research informs the question wording only.

## Repo layout

```
CLAUDE.md                  operating instructions for agents
events/events.csv          master event list
events/<slug>/             per event notes and captured people
companies/companies.csv    deduped companies, headcount verification columns
people/people.csv          curated 79 priority targets
people/pool/pool.csv       full pool, 2,456 people with Apollo IDs
people/drafts/             outreach drafts land here
prompts/01..05             the exact prompt for each stage, rerunnable
tools/parse_apollo.py      Apollo search JSON → pool.csv
```

## How to work this repo

1. Read `CLAUDE.md`.
2. Check status columns in `people/people.csv` and `people/pool/pool.csv` for unclaimed work (`enrichment_status = pending`).
3. Follow the stage prompt in `prompts/` for whatever stage you are running. The prompts are written to be executed verbatim by an agent.
4. Commit results back with the status columns updated.

## Hard rules

* No invented names, titles, or emails. Empty beats guessed.
* Every captured person and company carries a source.
* Headcount requires three source agreement before it is written.
* All work is attributed to Ranch Lab.
