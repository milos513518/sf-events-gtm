# Stage 1: Speaker and attendee extraction

Input: one row of `events/events.csv`. Output: `events/<slug>/speakers.csv` and `events/<slug>/event.md`.

## By event type

**Conference with published roster** (AI Engineer Code Summit, QCon SF, Microsoft Ignite, Fortune Brainstorm AI):
1. Fetch the speakers/agenda page from the event URL.
2. QCon and Ignite: capture only speakers in relevant tracks (Developer Experience, Platform Engineering, AI upskilling, engineering productivity). Record the track in `notes`.
3. Capture: name, title, company, session title, source URL.

**Luma event**:
1. Fetch the public page: hosts and any featured speakers are visible without login.
2. Guest list: only visible when registered and logged in. This is a browser agent task (Hyperagent or Claude in Chrome with Milos's session). Scroll the full guest list, capture name plus whatever title/company Luma shows. Mark `role_at_event = attendee`.
3. Note in `event.md` whether the guest list was swept and on what date. Re-sweep 2 to 3 days before the event; attendance fills late.

**Invite-only, no public roster** (Cerebral Valley, ELC dinner, Vercel CTO Circle):
1. Search news coverage and LinkedIn posts: "speaking at", "attending", "hosting" plus the event name.
2. Mark captures as `role_at_event = unknown` with the source URL. Lower confidence is acceptable here; flag in notes.

## speakers.csv schema

```
name,title,company,role_at_event,session,source_url,captured_date,notes
```

Rules: no invented data; empty field over guessed field; one row per person per event.
