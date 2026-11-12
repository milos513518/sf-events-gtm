# Stage 5: Outreach drafting

Input: `people/people.csv` rows with `enrichment_status = enriched` and `outreach_status = none`.

## Template (L&D / enablement outreach)

> Hi [Name], hope all is well. I was wondering, how does [team] help accelerate [company's AI initiative name] internally? And has [relevant pressure] changed how you design and deliver learning programs themselves? I'd love to compare notes.

Rules:

* Never open with a research fact. Research informs the question wording only ([company's AI initiative name], [relevant pressure]).
* Every draft includes a clearly labeled subject line, easy to copy and paste.
* No raw URLs in email bodies; hyperlinked anchor text only.
* Bullet format for any data points: proper bullet symbols, "• [Company name hyperlinked]: One sentence description. Metric 1, metric 2, metric 3."
* No em dashes, en dashes, or hyphens as punctuation anywhere.
* If the person appears on a guest list for an event Milos is attending, the draft references meeting at the event instead of asking for a call.
* Set `outreach_status = drafted` and store the draft in `people/drafts/<name-slug>.md`.
