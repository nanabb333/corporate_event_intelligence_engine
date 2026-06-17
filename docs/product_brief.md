# Corporate Event Intelligence Engine: Sprint 1 Product Brief

## Product Goal

The Corporate Event Intelligence Engine helps users ask evidence-based questions about corporate events and receive historical analogs, observed pathways, source references, and analyst-style notes.

Sprint 1 focuses only on CEO departure cases. The objective is to create a credible evidence base before retrieval, dashboards, similarity scoring, or LLM integration are introduced.

## Target User

The MVP is designed for business analysts, corporate strategy teams, risk analysts, research teams, and product users who need structured context around high-profile corporate leadership events.

The product answers descriptive questions such as:

- What has usually happened after abrupt CEO departures?
- What pathways have followed crisis-linked CEO exits?
- How do planned successions differ from board-led replacements?
- What historical analogs help frame a founder CEO stepdown?

## Non-Goals

The Sprint 1 evidence base does not:

- forecast future performance
- recommend buying, selling, or holding securities
- produce price targets
- rank stocks or companies
- predict event outcomes
- build retrieval logic
- build a dashboard
- build similarity scoring
- build LLM integration

## Sprint 1 Product Contract

Every CEO departure case must include:

- a clearly named company and ticker
- an event date
- a departure type
- a factual context summary
- an observed pathway label
- at least one source URL
- a descriptive analyst note

The analyst note must interpret the historical case without making predictions or recommendations.

## Proposed Case List

The Sprint 1 seed library includes 15 high-profile CEO departure cases:

| event_id | company | departure type | observed pathway |
|---|---|---|---|
| CEODEP001 | Apple | planned succession | continuity succession |
| CEODEP002 | Microsoft | planned succession | strategic reset |
| CEODEP003 | General Electric | planned succession | portfolio reset |
| CEODEP004 | Twitter | founder stepdown | founder transition |
| CEODEP005 | Starbucks | planned succession with founder return | interim founder return |
| CEODEP006 | The Walt Disney Company | performance-driven termination with predecessor return | board-led reset |
| CEODEP007 | Uber | abrupt resignation under investor pressure | governance repair |
| CEODEP008 | Boeing | crisis-linked termination | crisis accountability |
| CEODEP009 | Wells Fargo | crisis-linked resignation | reputational repair |
| CEODEP010 | McDonald's | conduct-related termination | conduct accountability |
| CEODEP011 | Intel | performance-driven replacement | operational reset |
| CEODEP012 | Ford | performance-driven replacement | strategic acceleration |
| CEODEP013 | Hewlett-Packard | conduct-related resignation | governance enforcement |
| CEODEP014 | Papa John's | founder resignation under reputational pressure | reputational repair |
| CEODEP015 | WeWork | founder resignation under board and investor pressure | governance repair |

## Source Reference Policy

The case library uses company announcements where available. When company source pages are unavailable or insufficiently specific, reputable business press or wire services are used.

All source references used for Sprint 1 are documented in `data/corporate_events_seed.csv` through the `source_url` field.

## Evidence Quality Rules

Each case should be reviewed against four questions:

1. Is the departure date clearly documented?
2. Is the departure type defensible from the source and context?
3. Is the pathway label descriptive rather than predictive?
4. Does the analyst note avoid recommendation, forecast, and price-target language?

## Next Milestone

The next milestone is evidence QA:

- verify each source URL manually
- confirm dates against at least one primary or reputable secondary source
- standardize sector names
- add a second source URL column if a case requires separate primary and secondary support
- freeze the Sprint 1 seed file before retrieval work begins
