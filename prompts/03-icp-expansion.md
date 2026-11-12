# Stage 3: ICP expansion per company

Input: one row of `companies/companies.csv`. Output: rows appended to `people/people.csv`.

1. Apollo people search (`mixed_people_api_search`) scoped to the company domain.
2. Title keywords (run as one query with OR groups, or split if result caps hit):
   * program manager, technical program manager
   * implementation, onboarding
   * enablement
   * learning and development, learning experience
   * developer experience, developer productivity, developer relations
   * platform engineering, internal tools
3. Seniority filter: manager, senior, director, head, VP. Record the level in `seniority`; flag director+ as `director_plus = true` in notes if useful.
4. Assign `icp_category` from the title: TPM | implementation | onboarding | enablement | L&D | DevEx | platform | devrel.
5. Deduplicate against existing `people/people.csv` rows by name plus company before appending.
6. Where Apollo returns fewer than 3 people for a company with 200+ employees, run an Exa/web search pass ("[company] enablement manager" etc.) and capture LinkedIn profile URLs.
7. Set `enrichment_status = pending` on every new row.
