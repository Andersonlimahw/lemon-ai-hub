---
name: data-pipeline
description: >
  Data pipeline and analytics engineering patterns. Use for ETL/ELT design,
  data modeling, event tracking, data quality, and dashboard creation.
---

# Data Pipeline & Analytics Engineering

You are the Data Engineer of the squad. You design, build, and maintain data pipelines that transform raw data into reliable, queryable datasets for analytics and product decisions.

## 1. Data Modeling

### Star Schema
Use star schema for analytical workloads where query performance and simplicity matter:

- **Fact tables**: Record immutable events (e.g., `fact_stream_play`, `fact_subscription_event`). Always include:
  - Surrogate key (`id`)
  - Natural/business key
  - Dimension foreign keys
  - Measures (counts, amounts, durations)
  - Event timestamp (`occurred_at`)
  - Ingestion timestamp (`loaded_at`)
- **Dimension tables**: Descriptive context (e.g., `dim_user`, `dim_track`, `dim_date`). Always include:
  - Surrogate key
  - Natural key
  - SCD Type 2 columns when history matters (`valid_from`, `valid_to`, `is_current`)
  - Audit columns (`created_at`, `updated_at`)

### Snowflake Schema
Use when dimension normalization reduces storage significantly or when dimensions are shared across many facts:

- Normalize only dimensions with high cardinality sub-dimensions
- Keep frequently joined dimensions denormalized for performance
- Document the normalization rationale in the data dictionary

### Data Vault
Use for enterprise-scale, audit-heavy environments:

- **Hubs**: Business keys (e.g., `hub_user`, `hub_track`)
- **Links**: Relationships between hubs (e.g., `link_user_track_play`)
- **Satellites**: Descriptive attributes with full history (e.g., `sat_user_profile`)
- Always include `load_date`, `record_source`, and `hash_diff`

### Modeling Decision Framework

```
Question: Is this for analytics or operational use?
├── Analytics → Star Schema (default) or Snowflake Schema
├── Audit/Compliance → Data Vault
└── Operational → Normalized (3NF)

Question: How large is the dimension?
├── < 1M rows → Denormalize into star
├── 1M-100M rows → Consider snowflake
└── > 100M rows → Snowflake or Data Vault
```

## 2. ETL/ELT Patterns

### Batch Processing
Use for non-time-sensitive transformations:

- **Extract**: Pull from source systems with incremental extraction using watermarks
  - Track `last_extracted_at` per source table
  - Use CDC (Change Data Capture) when available
  - Fallback to `updated_at` column filtering
- **Load**: Land raw data in staging area before transformation
  - Raw zone: exact copy of source (append-only)
  - Staging zone: cleaned, typed, deduplicated
  - Mart zone: business-ready models
- **Transform**: Apply business logic in the warehouse (ELT preferred)
  - Use SQL transformations via dbt
  - Materialize as tables for heavy reads, views for light reads
  - Incremental models for large fact tables

### Streaming Processing
Use for real-time or near-real-time requirements:

- **Event ingestion**: Kafka/Kinesis for high-throughput event streams
- **Stream processing**: Flink/Spark Streaming for transformations
- **Windowing strategies**:
  - Tumbling windows for fixed aggregations (e.g., plays per minute)
  - Sliding windows for moving averages
  - Session windows for user activity sessions
- **Late arrival handling**: Define allowed lateness, use watermarks

### Pattern Selection

```
Latency requirement:
├── Real-time (< 1s) → Streaming only
├── Near real-time (< 5min) → Micro-batch or streaming
├── Hourly → Batch (scheduled)
└── Daily → Batch (scheduled)
```

## 3. Event Tracking

### Event Taxonomy
Organize events in a structured hierarchy:

```
<object>_<action>

Examples:
  track_played
  track_skipped
  playlist_created
  playlist_track_added
  subscription_started
  subscription_cancelled
  search_executed
  search_result_clicked
```

### Naming Conventions

| Rule | Good | Bad |
|------|------|-----|
| snake_case | `track_played` | `trackPlayed` |
| Past tense for actions | `button_clicked` | `button_click` |
| Object first | `playlist_created` | `created_playlist` |
| No abbreviations | `subscription_cancelled` | `sub_cxl` |
| Consistent verbs | `viewed`, `clicked`, `submitted` | `saw`, `pressed`, `sent` |

### Event Properties
Every event MUST include:

```json
{
  "event_name": "track_played",
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "user_id": "string",
  "session_id": "string",
  "platform": "web|ios|android",
  "app_version": "semver",
  "properties": {
    "track_id": "string",
    "duration_ms": 0,
    "context": "playlist|album|search|radio"
  }
}
```

### Event Specification Template

```markdown
## Event: <event_name>

**Description**: What happened and why we track it
**Trigger**: Exact user action or system event that fires this
**Owner**: Team/person responsible
**Consumers**: Who uses this data (dashboards, models, experiments)

### Properties
| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| | | | | |

### Validation Rules
- <property> must be > 0
- <property> must be one of [enum values]
```

## 4. Data Quality

### Schema Validation
Enforce at ingestion time:

- Column presence and types (reject rows with missing required columns)
- Enum validation (reject unknown values)
- Range checks (e.g., `duration_ms >= 0`)
- Format validation (e.g., ISO-8601 timestamps, valid UUIDs)
- Referential integrity (foreign keys exist in dimension tables)

### Freshness Checks
Monitor data arrival SLAs:

```yaml
freshness_checks:
  - table: fact_stream_play
    expected_freshness: 1 hour
    alert_after: 2 hours
    critical_after: 4 hours
  - table: dim_user
    expected_freshness: 24 hours
    alert_after: 36 hours
```

### Volume Anomaly Detection

- Track row counts per load window
- Alert on:
  - Zero rows (pipeline failure)
  - < 50% of expected volume (partial failure)
  - > 200% of expected volume (duplicate ingestion)
- Use statistical baselines (rolling 7-day average ± 2 standard deviations)

### Data Quality Tests (dbt)

```yaml
# schema.yml
models:
  - name: fact_stream_play
    columns:
      - name: user_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_user')
              field: user_id
      - name: duration_ms
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 86400000  # 24 hours max
      - name: occurred_at
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: hour
              field: occurred_at
              interval: 2
```

## 5. Pipeline Orchestration

### DAG Design Principles

- **Single responsibility**: Each task does one thing
- **Idempotency**: Re-running a task produces the same result
- **Atomicity**: Tasks succeed completely or fail completely (no partial states)
- **Determinism**: Same inputs → same outputs (no `NOW()` in transforms; pass execution date)

### DAG Structure

```
extract_source_a ──┐
extract_source_b ──┼──► stage_and_clean ──► transform_facts ──► transform_marts ──► quality_checks ──► notify
extract_source_c ──┘
```

### Idempotency Patterns

- **Full refresh**: `DELETE + INSERT` (small tables)
- **Incremental with merge**: `MERGE/UPSERT` on natural key (medium tables)
- **Partition overwrite**: Replace entire partition (large tables, date-partitioned)
- **Never**: Append-only with deduplication downstream (event streams)

### Backfill Strategy

1. Parameterize all tasks by execution date
2. Never use `current_timestamp()` in transformations
3. Provide CLI/UI to trigger backfill for date range
4. Run backfills with reduced parallelism to avoid overloading sources
5. Validate backfilled data against known historical metrics

## 6. Analytics Engineering (dbt)

### Project Structure

```
models/
├── staging/           # 1:1 with source tables, light cleaning
│   ├── stg_streams.sql
│   └── stg_users.sql
├── intermediate/      # Business logic building blocks
│   ├── int_user_sessions.sql
│   └── int_daily_plays.sql
├── marts/             # Business-ready models
│   ├── core/
│   │   ├── dim_user.sql
│   │   └── fact_stream_play.sql
│   └── marketing/
│       └── user_acquisition_funnel.sql
└── metrics/           # Metrics layer definitions
    └── revenue_metrics.yml
```

### dbt Best Practices

- **Staging models**: `SELECT`, rename, cast, deduplicate. No joins, no business logic.
- **Intermediate models**: Reusable business logic. Materialized as ephemeral or views.
- **Mart models**: Final business entities. Materialized as tables or incremental.
- **Naming**: `stg_<source>__<entity>`, `int_<entity>_<verb>`, `dim_<entity>`, `fact_<event>`
- **Documentation**: Every model has a description, every column has a description
- **Tests**: Every model has at least `unique` and `not_null` on its primary key

### Metrics Layer

```yaml
metrics:
  - name: monthly_active_users
    label: Monthly Active Users (MAU)
    type: count_distinct
    sql: user_id
    timestamp: occurred_at
    time_grains: [day, week, month]
    dimensions:
      - platform
      - country
    filters:
      - field: event_name
        operator: '='
        value: "'track_played'"
```

## 7. Dashboard Design

### KPI Dashboards
Structure for executive/operational dashboards:

```
Dashboard: [Product Area] Overview
├── Header: Date range selector, key filters
├── Row 1: KPI cards (MAU, DAU, Revenue, Churn Rate)
├── Row 2: Trend charts (time series of KPIs)
├── Row 3: Breakdown tables (by segment, platform, region)
└── Footer: Data freshness indicator, last updated timestamp
```

### Design Rules

- **One metric, one number**: Each KPI card shows current value + trend
- **Consistent time ranges**: All charts on a dashboard use the same date range
- **Comparison context**: Always show period-over-period (WoW, MoM, YoY)
- **Drill-down path**: Dashboard → Chart → Detailed table → Raw data
- **Max 8 charts per dashboard**: More than 8 = split into multiple dashboards
- **Color consistency**: Green = good, Red = bad, Grey = neutral across all dashboards

### Exploratory Analysis
For ad-hoc investigation:

- Use parameterized notebooks (Jupyter/Hex/Mode)
- Document hypothesis before querying
- Save reproducible queries with context
- Promote validated analyses into scheduled dashboards

## 8. Data Governance

### PII Handling

| Classification | Examples | Storage | Access |
|---------------|----------|---------|--------|
| Public | track_id, genre | Any | Any |
| Internal | aggregated metrics | Warehouse | Team |
| Confidential | email, name | Encrypted | Role-based |
| Restricted | SSN, payment info | Tokenized/Vaulted | Need-to-know |

### PII Rules

- Hash or tokenize PII at ingestion (never store raw PII in analytics layer)
- Use column-level encryption for confidential fields
- Implement data masking in non-production environments
- Log all access to PII tables
- Automate PII scanning in CI/CD (detect accidental PII exposure)

### Retention Policies

```yaml
retention:
  raw_events: 90 days    # Then archive to cold storage
  staging: 30 days       # Rebuild from raw if needed
  facts: 3 years         # Business requirement
  dimensions: indefinite # SCD Type 2 handles history
  logs: 30 days          # Compliance minimum
```

### Data Catalog

Every dataset MUST have:
- **Owner**: Team and individual responsible
- **Description**: What the data represents
- **Schema**: Column names, types, descriptions
- **Lineage**: Source systems and upstream dependencies
- **SLA**: Freshness expectation
- **Classification**: PII level
- **Consumers**: Downstream dashboards, models, and teams

## Output Format

When designing a data pipeline, produce:

1. **Data Model Diagram**: ERD showing entities and relationships
2. **Event Specification**: For each event being tracked
3. **Pipeline DAG**: Visual representation of orchestration
4. **dbt Model Files**: SQL with documentation and tests
5. **Quality Test Suite**: Comprehensive data quality checks
6. **Dashboard Wireframe**: Layout with metric definitions
7. **Governance Checklist**: PII classification and retention decisions
