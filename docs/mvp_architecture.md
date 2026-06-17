# Corporate Event Intelligence Engine: MVP Architecture

## Sprint 1 Boundary

Sprint 1 creates the CEO Departure Case Library only.

In scope:

- `data/corporate_events_seed.csv`
- `data/event_taxonomy.yaml`
- `data/pathway_labels.yaml`
- `docs/product_brief.md`
- `docs/mvp_architecture.md`

Out of scope:

- retrieval
- dashboard
- similarity scoring
- LLM integration
- forecasting
- investment recommendations
- price targets

## MVP Architecture Overview

```text
Corporate Event Intelligence Engine

1. Evidence Base
   - Structured corporate event cases
   - Source URLs
   - Departure types
   - Observed pathway labels
   - Analyst notes

2. Event Taxonomy
   - Defines CEO departure as Sprint 1 event type
   - Defines allowed departure types
   - Marks earnings misses and product recalls as future scope

3. Pathway Label System
   - Converts event history into observed descriptive pathways
   - Avoids outcome prediction
   - Supports later analog retrieval and synthesis

4. Evidence QA Layer
   - Confirms dates, source links, and labels
   - Checks analyst notes for prohibited forecasting or recommendation language

5. Future Product Layers
   - Retrieval
   - Similarity scoring
   - Analyst synthesis
   - User-facing application
```

## Schema

The Sprint 1 CSV schema is:

| field | purpose |
|---|---|
| event_id | Stable unique identifier for each CEO departure case |
| company | Company name at time of event |
| ticker | Public ticker associated with the company |
| sector | High-level business sector |
| event_type | Corporate event category; Sprint 1 uses CEO departure |
| event_date | Date of public CEO departure announcement |
| departure_type | Descriptive type of CEO exit |
| context | Factual description of surrounding conditions |
| observed_pathway | Historical pathway label from `pathway_labels.yaml` |
| source_url | Source reference supporting the event record |
| analyst_note | Descriptive interpretation of the historical case |

## Taxonomy

Sprint 1 supports one event type:

```text
ceo_departure
```

Supported departure types:

- planned succession
- abrupt resignation
- founder stepdown
- founder return
- activist pressure
- crisis-linked departure
- performance-driven replacement
- conduct-related departure

Future event types:

- earnings miss
- product recall

## Pathway Labels

Sprint 1 labels historical CEO departure pathways, not future outcomes.

Core pathway labels:

- continuity succession
- strategic reset
- portfolio reset
- founder transition
- interim founder return
- board-led reset
- governance repair
- crisis accountability
- reputational repair
- conduct accountability
- operational reset
- strategic acceleration
- governance enforcement

## Sprint 1 Evidence Base Plan

### Step 1: Freeze the Schema

Big picture: The schema is the contract for every case in the evidence base.

Why it matters: Without a stable schema, later retrieval and synthesis layers will inherit inconsistent case data.

Where it fits: The schema sits between raw source research and future product logic.

Next milestone: Confirm whether Sprint 1 needs a second source field before data QA begins.

### Step 2: Validate the 15 Cases

Big picture: The seed library should favor source quality and event variety over quantity.

Why it matters: The first case set teaches the product how to distinguish planned succession, crisis departure, founder transition, conduct issue, and performance reset.

Where it fits: This is the historical evidence layer that later analog retrieval will query.

Next milestone: Review all 15 rows for date accuracy, source accessibility, and label consistency.

### Step 3: Normalize Labels

Big picture: Departure types describe why or how the CEO exited; pathway labels describe what corporate pattern the case represents.

Why it matters: Keeping these separate prevents the product from confusing event cause with observed corporate response.

Where it fits: Taxonomy supports classification; pathway labels support historical interpretation.

Next milestone: Lock the initial label set and avoid adding synonyms until enough cases justify them.

### Step 4: QA Analyst Notes

Big picture: Analyst notes should explain historical meaning without forecast language.

Why it matters: This keeps the product positioned as corporate intelligence, not investment advice.

Where it fits: Analyst notes are the future narrative layer's raw material.

Next milestone: Run a prohibited-language review for terms such as buy, sell, hold, price target, will outperform, and should invest.

### Step 5: Prepare for Sprint 2

Big picture: Sprint 2 should only begin once the CEO departure evidence base is clean enough to reuse.

Why it matters: Retrieval and synthesis will amplify any ambiguity in the source data.

Where it fits: Sprint 1 becomes the foundation for future event types and product workflows.

Next milestone: Add QA status fields or a second source field if the product needs stronger auditability before retrieval begins.
