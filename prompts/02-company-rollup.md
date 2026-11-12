# Stage 2: Company rollup and enrichment

Input: all `events/*/speakers.csv`. Output: `companies/companies.csv`.

1. Collect every distinct company across all speaker files. Normalize names (strip Inc, legal suffixes; resolve obvious aliases like "GitHub" vs "GitHub, Inc.").
2. One row per company. `events` column lists every event slug where the company appears; `speaker_count` counts its people captured so far.
3. Enrich via Apollo organizations endpoint: domain, industry.
4. Headcount verification, in this exact order, and write each source's number to its own column:
   * `headcount_apollo` from Apollo
   * `headcount_pdl` from People Data Labs
   * `headcount_linkedin` from the LinkedIn company page (browser agent)
   * `headcount_verified = true` and `employee_count` filled only when all three agree (same declared range counts as agreement)
5. Priority order for stage 3: companies appearing at multiple events first, then companies with the most captured people.
