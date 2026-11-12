# SF Events GTM Pipeline

Ranch Lab pipeline: SF Bay Area events (Nov to Dec 2026) → speakers and attendees → companies → ICP individuals → enriched outreach targets.

Any agent opening this repo: read this file fully, then check `people/people.csv` status columns to find unclaimed work. Never double-work a row that another agent has already moved past `pending`.

## Repo layout

```
events/events.csv          master event list (30 events; status: confirmed | watchlist)
events/<slug>/event.md     per-event notes: registration status, logistics, guest list availability
events/<slug>/speakers.csv people captured at that event (speakers, hosts, attendees)
companies/companies.csv    deduped companies, enriched and headcount-verified
people/people.csv          master target list across all events
prompts/                   stage prompts; rerun a stage by following its prompt exactly
```

## Pipeline stages

1. **Speaker/attendee extraction** (per event). Conference sites: fetch published speaker pages. Luma events: public page gives hosts and featured speakers; the guest list requires a logged-in registered session (browser agent job). Invite-only events: reconstruct from news coverage and LinkedIn posts.
2. **Company rollup.** Dedupe into `companies/companies.csv`. Enrich via Apollo organizations endpoint.
3. **ICP expansion.** For each company, Apollo people search with the ICP titles below. Append to `people/people.csv`.
4. **Per-person enrichment.** LinkedIn activity, recent posts, event attendance cross-reference, company AI initiative names.
5. **Outreach drafting.** Follow `prompts/05-outreach.md`. Research informs question wording only; never open a message with a research fact.

## ICP titles (stage 3 search terms)

Program Manager, Technical Program Manager, TPM, Implementation Manager, Implementation Lead, Onboarding Manager, Customer Onboarding, Enablement (Sales Enablement, Field Enablement, Engineering Enablement, Revenue Enablement), Learning and Development, L&D, Learning Experience, Developer Experience, DevEx, Developer Productivity, Platform Engineering (lead/manager/director), Developer Relations, Internal Tools.

Seniority: manager and above. Flag director+ separately (column `seniority`).

## Hard rules

* Employee counts: verify with three sources in order, Apollo first, then People Data Labs, then LinkedIn. All three must agree before the number is written to `companies.csv`. Apollo alone is not trusted.
* Every captured person and company carries a `source_url`.
* Never invent names, titles, or emails. A field you cannot verify stays empty.
* All work is attributed to Ranch Lab.

## people.csv schema

```
name,title,company,company_domain,seniority,icp_category,events,role_at_event,linkedin_url,email,email_status,enrichment_status,outreach_status,source_url,notes
```

Status values:
* enrichment_status: pending | in_progress | enriched
* outreach_status: none | drafted | sent | replied
* role_at_event: speaker | host | attendee | unknown

## companies.csv schema

```
company,domain,industry,employee_count,headcount_apollo,headcount_pdl,headcount_linkedin,headcount_verified,events,speaker_count,notes
```

`employee_count` stays empty until `headcount_verified` is true (all three sources agree).
