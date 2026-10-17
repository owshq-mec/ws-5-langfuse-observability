# Orbisa — story bible

Orbisa, Brisklane, Helix and every person, customer and number in this folder are fictional.
They exist to teach context engineering and observability. Any resemblance to real companies is
coincidental.

This file is the single source of truth for the corpus. Every source file and every ground-truth
answer in `truth/questions.jsonl` must agree with it.

## The company

| Fact | Value |
|---|---|
| Name | Orbisa |
| What it sells | B2B logistics SaaS: **Orbisa Track** (shipment tracking API and dashboard) and **Orbisa Bill** (freight billing and audit) |
| Customers | Mid-size freight distributors and wholesalers |
| Founded | April 2019, Austin, Texas |
| Founders | Marina Costa (CEO), Daniel Okafor (CTO) |
| Employees | About 420 (October 2026) |
| Funding | Series A 2021, Series B USD 48M in March 2024 |
| Acquisition | **Brisklane** (Lisbon, last-mile routing, about 60 people), closed 2025-03-10 |
| Internal context engine | **Helix** (built in 2026 to answer questions across all internal systems) |

## Plans

| Plan | Price | Notes |
|---|---|---|
| Starter | USD 500 per month | Annual or monthly |
| Growth | USD 2,400 per month | Annual |
| Enterprise | Custom, from USD 12,000 per month | Annual, 99.9% monthly uptime SLA (POL-012) |

There is no Platinum plan.

## People

| Person | Role | Aliases in the systems |
|---|---|---|
| Marina Costa | CEO | Slack `marina` |
| Daniel Okafor | CTO | Slack `daniel.o` |
| Priya Raman | CFO | Slack `priya` |
| Tomás Herrera | Head of RevOps | Slack `tomas.h` |
| Rafael Mendes | Sales Director | Slack `rafa` |
| Johanna Lindqvist | Senior Account Executive | **Slack `jo.l` (display "Jo L.")**, HubSpot "Johanna Lindqvist", Gong "Johanna Lindqvist", Zendesk "Jo Lindqvist" |
| Owen Brandt | Account Executive | Slack `owen` |
| Aisha Bello | VP Customer Success | Slack `aisha` |
| Ken Watanabe | Support Lead | Slack `ken.w`, Zendesk "Ken Watanabe" |
| Sam Patel | Support Agent | Zendesk "Sam Patel" |
| Nadia Silva | Data Platform Lead | Slack `nadia` |
| Ingrid Holm | Site Reliability Engineer | Slack `ingrid` |
| Luca Ferretti | Brisklane founder, now Director of Routing Product | Slack `luca`, Notion "Luca" |

## Customers

| Customer | Plan | ARR (USD) | Contract paper | Last / next renewal | Owner |
|---|---|---|---|---|---|
| Orion Freight Systems | Enterprise | 186,000 | Orbisa MSA with clause 7.3 | renewed 2026-08-15 | Johanna Lindqvist |
| Kodiak Cold Chain | Enterprise | 240,000 | Orbisa | renews 2026-11-30 (at risk) | Johanna Lindqvist |
| Bluefin Distribution | Growth | 28,800 | Orbisa standard | renewed 2026-10-03 | Owen Brandt |
| Cedar & Pine Wholesale | Starter | 6,000 (until churn) | **Brisklane legacy** until 2027-01-31 | renewed 2026-02-01, cancelled with a full refund on 2026-03-06 (former customer) | Owen Brandt |

Customer contacts: Dana Whitfield (Orion, VP Operations), Marcus Ellery (Orion, Procurement),
Hal Brennan (Kodiak, COO), Sofia Ruiz (Bluefin, Finance Manager), Tom Avery (Cedar & Pine, Owner).

## Timeline of facts that change

| Date | What changed | Where it is recorded | Where the old version still lives |
|---|---|---|---|
| 2023-02-01 | Refund Policy v1 (POL-007): annual plans get a **pro-rata** refund within **30 days** of renewal, approved by **Finance (CFO)** | Confluence "Refund Policy (2023)" | — |
| 2025-03-10 | Orbisa acquires Brisklane | Slack #announcements | — |
| 2025-06-02 | Discount matrix: AE up to 10%, Sales Director up to 20%, **CFO above 20%** | Confluence "Discount Approval Matrix" | — |
| 2025-07-01 | Cedar & Pine signs a migration addendum: Brisklane terms stay until 2027-01-31 | Drive PDF | — |
| 2025-11-02 | Revenue team page lists "Refund approvals: Finance (Priya Raman)" | Confluence "Revenue Team — Roles" | becomes stale on 2026-03-03 |
| 2025-11-04 | Retention unified: **24 months for all customers including Brisklane**, effective 2026-01-01 | Slack #data-platform, Confluence "Data Retention Policy" v3 (2025-12-15) | Notion "Data Retention" still says 12 months |
| 2026-03-01 | Refund & Credits Policy v2 (POL-007 v2) takes effect: **full refund within 14 days** of an annual renewal, after that service credits only; contract terms override; Brisklane legacy contracts keep Brisklane terms until their first Orbisa-paper renewal; approvals by **RevOps** | Confluence "Refund and Credits Policy" (published 2026-02-20) | Confluence "Refund Policy (2023)" was never archived |
| 2026-03-03 | Refund approvals move from Finance to **RevOps — Tomás Herrera approves every refund**; Finance only pays out | Slack #revops (Priya) | Confluence "Revenue Team — Roles" |
| 2026-06-15 | Discounts **above 20% need CEO and CFO** sign-off | Slack #sales (Marina) | Confluence "Discount Approval Matrix" |

Brisklane's own terms (Notion "Refunds and Cancellations"): full refund within **60 days** of a
renewal, no questions asked. They apply only to Brisklane legacy contracts.

## The Orion story (the anchor case)

1. 2025-08-15: Orion signs the Orbisa MSA and Order Form OF-2025-0815. Enterprise, USD 186,000 per
   year (USD 15,500 per month), auto-renews every 12 months. **Clause 7.3**: if Orbisa misses the
   Uptime SLA (Schedule B, 99.9% monthly) in any calendar month during the 60 days after a renewal
   date, Orion may request a pro-rata refund of the remaining term within 60 days of that renewal.
2. 2026-08-15: the contract renews.
3. 2026-08-19: **INC-2291**, Tracking API outage, 3 h 12 min, a bad deploy of tracking-ingest
   v4.12 caused Kafka consumer lag. Zendesk #48190.
4. 2026-08-27: **INC-2304**, Tracking API outage, 1 h 47 min, an expired TLS certificate on the
   carrier-webhook gateway. Zendesk #48207.
5. August 2026 Tracking API uptime: (744 h − 4.98 h) / 744 h = **99.33%**. That breaches the 99.9%
   SLA. Under POL-012 the credit is **10% of the monthly fee = USD 1,550** (uptime between 99.0%
   and 99.9%), to be requested within 30 days of month end.
6. 2026-09-08: Q3 QBR call (Gong). Johanna promises a **service credit** if there is another
   tracking incident this quarter. She does **not** promise a refund. Dana says their legal team
   is reviewing the contract's SLA clause.
7. 2026-09-29 (45 days after renewal): Zendesk #48233, Orion asks for a refund. Sam Patel replies
   with the **stale 2023 rule** ("only within 30 days of renewal") and the ticket is escalated.
   No refund has been approved yet.

**Correct answer on 2026-09-29:** Orion is eligible for a **pro-rata refund under MSA clause 7.3**,
because the August SLA was breached inside the 60-day window and the request came on day 45.
The standard policy alone would say no (14-day window). The refund must be approved by
**Tomás Herrera (Head of RevOps)**, not Finance.

## The other cases

- **Kodiak**: on the 2026-10-02 call Hal Brennan asks for a 25% renewal discount (competitor
  "FleetGlass"). On 2026-10-06 in #deal-desk Rafael says the CFO can approve it; Tomás corrects him:
  since 2026-06-15, above 20% needs **Marina Costa (CEO) and Priya Raman (CFO)**.
- **Bluefin**: renewed 2026-10-03 on Orbisa standard terms. A refund request on 2026-10-13
  (day 10) gets a **full refund** under POL-007 v2, approved by RevOps.
- **Cedar & Pine**: Brisklane legacy. Refund request on 2026-03-05, 32 days after the 2026-02-01
  renewal, because they are cancelling. Eligible for a full refund under Brisklane terms (60 days).
  Ken escalated it, and Tomás approved it on 2026-03-06 (Zendesk #48102). HubSpot now lists them as
  a former customer; the read-only Brisklane Notion customer list still says "Active" (stale).
- **Bluefin refund**: Zendesk #48251 on 2026-10-13, escalated to RevOps, not approved yet.

## Systems and formats

| System | Folder | Format |
|---|---|---|
| Slack | `slack/` | Workspace export: `users.json`, `channels.json`, `<channel>/<YYYY-MM-DD>.json` |
| Confluence | `confluence/` | Space HTML export: `index.html` plus one HTML file per page |
| Notion (Brisklane) | `notion/` | Markdown & CSV export with 32-hex page ids |
| Google Drive | `drive/` | Signed contract PDFs |
| HubSpot | `hubspot/` | CRM CSV exports: companies, deals, contacts |
| Zendesk | `zendesk/` | Incremental ticket export, `users.json`, `comments/<ticket>.json` |
| Gong | `gong/` | `calls.json` (calls/extensive) and `transcripts.json` (calls/transcript) |

## Distractor documents

A real company is mostly noise. These files exist so retrieval has to work for its answer. None of them
changes any answer in `truth/questions.jsonl`.

| Kind | Files | Trap it sets |
|---|---|---|
| Near-miss | Confluence "Expense Reimbursement Policy" (Finance approves claims above USD 500) | Confused with refund approvals |
| Near-miss | Confluence "Application Log Retention" (debug logs 30 days, audit logs 13 months) | Confused with shipment-tracking retention |
| Near-miss | Confluence "Orbisa Track Release Notes 4.12", Slack `#eng-deploys` 2026-08-18 | The deploy behind INC-2291, without saying it failed |
| Near-miss | Gong "Pinecrest Logistics - Discovery call" (Enterprise from USD 12,000 per month, 99.9% SLA) | A prospect, not a customer |
| Noise | Confluence onboarding and PTO pages; Notion "Routing Algorithm Notes" and "Lisbon Office Guide"; Slack `#general`, `#random`, `#product`, `#support` (SSO macro) | Unrelated company knowledge |
| New customer | Mesa Ridge Foods (Growth, USD 28,800, started 2026-09-15, owner Owen Brandt), Slack `#sales` 2026-09-12, HubSpot rows, Zendesk #48240 (Okta SSO) | Extra customer that is not Enterprise and renews in 2027 |
| Other tickets | Zendesk #48120 (Bluefin CSV export), #48166 (Kodiak rate limit, 600 requests per minute) | Customer tickets unrelated to refunds |
| Contract | Drive "Mutual_NDA_Pinecrest_Logistics_2026-10-07.pdf" | A signed document that is not a customer contract |

## Known Helix weaknesses (facilitator only)

Observed in the graph built from this corpus. They are left in on purpose: the team should find them with
Langfuse, not read about them.

- Aliases are not merged: "Johanna Lindqvist", "Jo L." and "Jo (Orbisa sales)" end up as separate people (Q06).
- A later but wrong statement can close a correct fact: Rafa's outdated reply on 2026-10-06 marked the
  CEO + CFO discount rule as no longer valid (Q07).
- `read_source` has no as-of date: it returns a whole document, including any part written after the
  question's date (for example the full Zendesk thread).
- Future leaks through dates (found with Langfuse traces in the reference build, 2026-10-16): on an as-of date
  before a change, `search_context` still shows `valid_until` set by the later decision (Q09 on 2025-10-01 sees
  `valid_until: 2025-11-04`), `list_sources` lists every document with its date, and `read_source` returns
  combined files whole (all Gong calls, all HubSpot rows, the whole Zendesk thread). About half of the temporal
  answers mention a date they could not know (Q03 on 2025-12-01 cites the 2026-03-03 move to RevOps). A code
  score "answer mentions a date after as-of on which a source document was recorded" makes it measurable.
- Wrong end date: the 12-month Brisklane retention fact is closed on 2025-11-04 (the decision day), not on
  2026-01-01 (the effective date). `find_entities` summaries are built from all episodes regardless of date.
- HubSpot rows are dated by "Last Modified Date", so as of 2026-09-29 only 1 of 5 companies exists in Helix.
- Ground truth vs Helix paths: Helix serves `hubspot/deals.csv` and `hubspot/contacts.csv` inside
  `hubspot/companies.csv`, `gong/calls.json` inside `gong/transcripts.json`, and Zendesk tickets as
  `zendesk/comments/<id>.json`. Q09 and Q21 list expected sources recorded after their as-of date. Source-recall
  evaluators must map paths and skip later documents; the ground truth is left as it is.
