# Sprint 2 Implementation Plan

## Big Picture

Sprint 2 builds the first working Corporate Historical Analog Engine from the Sprint 1 CEO departure evidence base.

The deliverable is a deterministic workflow that answers:

> What usually happens after an abrupt CEO departure?

## Why It Matters

This sprint converts static research artifacts into a usable product behavior.

The goal is not a complete application. The goal is to prove that structured corporate event cases can produce a grounded, repeatable analyst brief.

## Where It Fits In The Product

Sprint 2 sits between evidence-base construction and future productization:

```text
Sprint 1: CEO Departure Case Library
Sprint 2: Historical Analog Engine
Sprint 3: Broader event questions and stronger retrieval QA
Future: interface, source expansion, and optional synthesis layers
```

## Implementation Scope

Built in Sprint 2:

- deterministic retrieval framework
- pathway aggregation layer
- analyst brief generator
- sample retrieval JSON
- sample CEO departure answer
- design and scoring documentation

Not built:

- dashboard
- LLM integration
- forecasting
- investment recommendations
- stock prediction
- price targets

## Files

Created:

- `src/historical_analog_engine.py`
- `docs/historical_analog_engine_design.md`
- `docs/retrieval_scoring_framework.md`
- `docs/sprint2_implementation_plan.md`
- `outputs/sample_retrieval_results.json`
- `outputs/sample_ceo_departure_answer.md`

Inputs:

- `data/corporate_events_seed.csv`
- `data/event_taxonomy.yaml`
- `data/pathway_labels.yaml`

## Demo Workflow

Run:

```bash
python3 src/historical_analog_engine.py
```

Output:

```text
outputs/sample_retrieval_results.json
outputs/sample_ceo_departure_answer.md
```

## Validation Plan

### Step 1: CSV Integrity

Confirm the case library parses correctly and contains the expected 15 cases.

### Step 2: Retrieval Output Integrity

Confirm the JSON output contains:

- question
- query profile
- scoring framework
- retrieved cases
- observed pathways
- limitations

### Step 3: Analyst Brief Integrity

Confirm the markdown brief contains:

- Question
- Historical Analogs
- Why These Cases Were Selected
- Observed Pathways
- Evidence Base
- Analyst Notes
- Limitations

### Step 4: Guardrail Review

Confirm the generated answer does not contain investment recommendations, stock predictions, or price targets.

## Next Milestone

The next milestone is to add a second deterministic demo question:

> What usually happens after a crisis-linked CEO departure?

That should use the same engine, query-profile pattern, and analyst brief structure before any interface or LLM layer is considered.
