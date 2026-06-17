# Historical Analog Engine Design

## Big Picture

Sprint 2 turns the CEO Departure Case Library into the first working Corporate Historical Analog Engine.

The engine answers one MVP question:

> What usually happens after an abrupt CEO departure?

The product remains descriptive. It retrieves comparable historical cases, groups them into observed pathways, and produces an analyst brief grounded in the source-backed case library.

## Why It Matters

The MVP needs to prove that the case library can support structured historical reasoning before any dashboard, LLM integration, or advanced retrieval layer is added.

This step matters because it creates the product's first reusable workflow:

```text
question
-> query profile
-> deterministic analog retrieval
-> pathway aggregation
-> analyst brief
-> limitations
```

## Where It Fits In The Product

Sprint 1 created the evidence base. Sprint 2 creates the first product behavior on top of that evidence base.

The analog engine sits between raw case data and the eventual user-facing experience:

```text
data/corporate_events_seed.csv
-> src/historical_analog_engine.py
-> outputs/sample_retrieval_results.json
-> outputs/sample_ceo_departure_answer.md
```

## System Components

### 1. Query Profile

The demo question is converted into a structured profile:

```yaml
event_type: CEO departure
departure_type: abrupt resignation
sector: ""
context: abrupt resignation CEO departure investor pressure board pressure governance culture controversy crisis founder scrutiny
observed_pathway: governance repair
```

The empty sector field means sector does not influence the Sprint 2 demo score.

### 2. Historical Analog Retrieval

Each case is scored using four evidence signals:

- departure type
- sector
- context
- observed pathway

The retrieval output is deterministic. The same seed CSV and query profile produce the same ranked result.

### 3. Pathway Aggregation

Retrieved cases are grouped by `observed_pathway`.

The aggregation layer answers:

- Which pathways appear in the retrieved analog set?
- How many cases support each pathway?
- Which companies are examples of each pathway?
- What is the descriptive interpretation of each pathway?

### 4. Analyst Brief Generator

The generated brief contains:

- Question
- Historical Analogs
- Why These Cases Were Selected
- Observed Pathways
- Evidence Base
- Analyst Notes
- Limitations

The brief is evidence-backed and avoids forecasts, recommendations, price targets, and stock predictions.

## Next Milestone

The next milestone is validation and expansion:

- QA the top retrieved cases for the demo question
- add a second source field if stronger auditability is needed
- test a second question such as crisis-linked CEO departure
- keep retrieval deterministic until the evidence base is larger
