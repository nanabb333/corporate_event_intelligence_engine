# Retrieval Scoring Framework

## Big Picture

The Sprint 2 retrieval framework ranks CEO departure cases using transparent rule-based scoring.

It is not semantic search, similarity scoring by embedding, or LLM reasoning. It is deterministic evidence matching over the Sprint 1 CSV fields.

## Why It Matters

The product needs explainable retrieval before it adds more sophisticated layers.

For an analyst product, users need to see why cases were selected. A transparent scoring system makes every analog auditable.

## Where It Fits In The Product

The scoring framework powers:

- `outputs/sample_retrieval_results.json`
- the "Historical Analogs" section
- the "Why These Cases Were Selected" section
- the pathway aggregation layer

## Score Components

Maximum base score: 100 points.

| component | max points | field used | purpose |
|---|---:|---|---|
| departure type | 35 | `departure_type` | prioritizes abrupt, pressured, crisis, founder, conduct, or board-action similarity |
| sector | 15 | `sector` | supports sector-specific retrieval when the query includes sector constraints |
| context | 25 | `context`, `departure_type`, `analyst_note` | captures deterministic keyword overlap |
| observed pathway | 25 | `observed_pathway` | favors exact or related pathway families |

## Departure Type Logic

Departure type is scored with tags:

- `abrupt_pressure`
- `founder`
- `planned`
- `crisis`
- `conduct`
- `performance`
- `board_action`

Exact departure-type matches receive the highest score. Related tags receive partial credit.

## Sector Logic

Sector only contributes when a query specifies a sector.

For the demo question, no sector is specified, so the sector score is zero for all cases. This avoids inventing a sector preference where the user did not ask for one.

## Context Logic

Context scoring uses deterministic keyword overlap after stopword removal and alias expansion.

Examples of alias groups:

- `pressure`: pressure, pressured, investor, activist, board, scrutiny
- `governance`: governance, board, controls, disclosure
- `crisis`: crisis, scandal, controversy, regulatory, safety
- `conduct`: conduct, misconduct, policy, investigation
- `performance`: performance, execution, operating, competitive, strategic

## Observed Pathway Logic

Exact pathway matches receive full credit.

Related pathways receive partial credit if they belong to the same pathway family.

Pathway families used in Sprint 2:

- accountability and repair
- leadership reset
- planned continuity
- founder transition

## Output Contract

Each retrieved case includes:

- event ID
- company
- ticker
- sector
- event date
- departure type
- observed pathway
- source URL
- analyst note
- total score
- score components
- selection reasons

## Next Milestone

The next milestone is retrieval QA:

- inspect whether the top 5 to 7 analogs are defensible
- tune only documented weights and tags
- avoid adding opaque scoring behavior
- keep scoring deterministic until the case library expands beyond the initial Sprint 1 dataset
