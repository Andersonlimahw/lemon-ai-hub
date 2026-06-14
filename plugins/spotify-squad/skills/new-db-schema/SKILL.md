---
name: new-db-schema
description: >
  Database schema design workflow. Use when creating or modifying database
  schemas, coordinating between backend, data, and QA engineers.
---

# New DB Schema — Database Schema Design Workflow

You are the Database Architect. You guide the creation and modification of database schemas with a focus on correctness, performance, safety, and zero-downtime migrations.

## Schema Design Pipeline

```
Requirements → Schema Design → Migration Strategy → Index Design
     │               │                │                  │
     ▼               ▼                ▼                  ▼
  Entities &     Normalization     Up/Down +          Query-driven
  Access         decisions         Zero-downtime      optimization
  Patterns

     → Validation Rules → Security → Testing → Documentation
            │                │          │            │
            ▼                ▼          ▼            ▼
        Constraints &    RLS + Enc   Migration    ERD + Data
        Triggers                     tests        Dictionary
```

## Phase 1: Requirements Analysis

### Entity Discovery

Identify all entities and their relationships:

```markdown
## Entity Analysis: <Feature Name>

### Entities
| Entity | Description | Estimated Volume | Growth Rate |
|--------|------------|-----------------|-------------|
| Playlist | User-created collection of tracks | 500M | 1M/day |
| PlaylistTrack | Track membership in playlist | 5B | 10M/day |
| PlaylistCollaborator | Shared editing access | 100M | 500K/day |

### Relationships
| Relationship | Type | Description |
|-------------|------|-------------|
| User → Playlist | 1:N | User owns many playlists |
| Playlist → Track | M:N | Playlists contain many tracks, tracks in many playlists |
| User → PlaylistCollaborator | 1:N | User can collaborate on many playlists |

### Entity Lifecycle
| Entity | Created When | Updated When | Deleted When | Soft Delete? |
|--------|-------------|-------------|-------------|-------------|
| Playlist | User creates | Title/desc change | User deletes | Yes |
| PlaylistTrack | Track added | Position changed | Track removed | No (hard) |
```

### Access Patterns

Define ALL queries this schema must support efficiently:

```markdown
## Access Patterns

### Read Patterns (ordered by frequency)
| # | Query | Frequency | Latency SLA | Pattern |
|---|-------|-----------|-------------|---------|
| R1 | Get playlist by ID with tracks | 10K/s | < 50ms | Point read + join |
| R2 | List user's playlists | 5K/s | < 100ms | Range scan by user_id |
| R3 | Search playlists by name | 1K/s | < 200ms | Full-text search |
| R4 | Get playlist collaborators | 500/s | < 50ms | Range scan by playlist_id |
| R5 | Check if track in playlist | 2K/s | < 20ms | Point read (composite key) |

### Write Patterns
| # | Operation | Frequency | Consistency | Pattern |
|---|-----------|-----------|-------------|---------|
| W1 | Create playlist | 100/s | Strong | Insert |
| W2 | Add track to playlist | 500/s | Strong | Insert + position update |
| W3 | Reorder tracks | 200/s | Strong | Batch position update |
| W4 | Delete playlist | 50/s | Eventual | Soft delete + async cleanup |

### Aggregation Patterns
| # | Query | Frequency | Freshness |
|---|-------|-----------|-----------|
| A1 | Playlist count per user | On profile view | < 1 min |
| A2 | Total tracks in playlist | On playlist view | Real-time |
| A3 | Most popular playlists | Dashboard | < 1 hour |
```

---

## Phase 2: Schema Design

### Normalization Decisions

Apply normalization rules, then make conscious denormalization decisions:

```markdown
## Normalization Analysis

### 3NF Schema (Starting Point)
\`\`\`sql
-- Fully normalized
CREATE TABLE playlists (
  id UUID PRIMARY KEY,
  owner_id UUID NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  is_public BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ  -- soft delete
);

CREATE TABLE playlist_tracks (
  id UUID PRIMARY KEY,
  playlist_id UUID NOT NULL,
  track_id UUID NOT NULL,
  position INTEGER NOT NULL,
  added_by UUID NOT NULL,
  added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(playlist_id, track_id)
);

CREATE TABLE playlist_collaborators (
  id UUID PRIMARY KEY,
  playlist_id UUID NOT NULL,
  user_id UUID NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'editor',  -- editor, viewer
  invited_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(playlist_id, user_id)
);
\`\`\`

### Denormalization Decisions
| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Add `track_count` to playlists | Avoid COUNT(*) on every playlist view (R1) | Must maintain on W2/track delete |
| Add `owner_name` to playlists | Avoid join on user table for R2 | Must update on username change (rare) |
| Do NOT embed tracks in playlist | Unbounded array, hard to query/paginate | Accept join cost for R1 |

### Final Schema
[Apply denormalization decisions to the 3NF schema]
```

### Column Design Rules

| Rule | Example | Rationale |
|------|---------|-----------|
| Always use UUID for PKs | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` | Globally unique, no sequence contention |
| Always add timestamps | `created_at`, `updated_at` | Audit trail, debugging |
| Use TIMESTAMPTZ not TIMESTAMP | `TIMESTAMPTZ` | Timezone-safe |
| Prefer VARCHAR(n) over TEXT for bounded fields | `title VARCHAR(200)` | Enforces limits at DB level |
| Use TEXT for unbounded content | `description TEXT` | No artificial limits |
| Use enums or check constraints for fixed values | `CHECK (role IN ('editor', 'viewer'))` | Data integrity |
| Soft delete with `deleted_at` | `deleted_at TIMESTAMPTZ` | Recovery, audit, cascade control |
| Never use SERIAL, use IDENTITY or UUID | `GENERATED ALWAYS AS IDENTITY` | Sequence issues in distributed systems |

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | snake_case, plural | `playlist_tracks` |
| Columns | snake_case, singular | `track_id` |
| Primary keys | `id` | `id UUID` |
| Foreign keys | `<referenced_table_singular>_id` | `playlist_id` |
| Timestamps | `<verb>_at` | `created_at`, `deleted_at` |
| Booleans | `is_<adjective>` or `has_<noun>` | `is_public`, `has_cover` |
| Indexes | `idx_<table>_<columns>` | `idx_playlist_tracks_playlist_position` |
| Constraints | `chk_<table>_<rule>` | `chk_playlist_title_length` |
| Unique constraints | `uq_<table>_<columns>` | `uq_playlist_tracks_playlist_track` |

---

## Phase 3: Migration Strategy

### Zero-Downtime Migration Rules

**NEVER** in a single migration:
- ❌ Rename a column (old code still references old name)
- ❌ Change a column type (may fail for existing data)
- ❌ Add a NOT NULL column without default (blocks for large tables)
- ❌ Drop a column that's still referenced

**ALWAYS** use multi-step migrations:

#### Adding a NOT NULL Column

```
Migration 1: Add column as NULLABLE with default
Migration 2: Backfill existing rows
Migration 3: Add NOT NULL constraint
Deploy: Code now reads/writes the column
Migration 4: (Optional) Remove default if not needed
```

#### Renaming a Column

```
Migration 1: Add new column
Migration 2: Backfill new column from old
Deploy: Code writes to BOTH columns, reads from new
Migration 3: Stop writing to old column
Migration 4: Drop old column
```

#### Changing a Column Type

```
Migration 1: Add new column with new type
Migration 2: Backfill with type conversion
Deploy: Code writes to BOTH, reads from new
Migration 3: Drop old column
```

### Migration File Template

```sql
-- Migration: YYYYMMDDHHMMSS_<descriptive_name>
-- Description: <what this migration does and why>
-- Reversible: Yes/No
-- Estimated duration: <time for largest table>
-- Locks acquired: <tables locked and duration>

-- ============================================
-- UP MIGRATION
-- ============================================

BEGIN;

-- Step 1: Create table / Add column
CREATE TABLE IF NOT EXISTS playlist_tracks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  playlist_id UUID NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
  track_id UUID NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  position INTEGER NOT NULL,
  added_by UUID NOT NULL REFERENCES users(id),
  added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_playlist_tracks_playlist_track UNIQUE(playlist_id, track_id),
  CONSTRAINT chk_playlist_tracks_position CHECK (position >= 0)
);

-- Step 2: Create indexes (CONCURRENTLY if possible, outside transaction)
-- NOTE: Run separately if using CONCURRENTLY
CREATE INDEX idx_playlist_tracks_playlist_position
  ON playlist_tracks(playlist_id, position);

CREATE INDEX idx_playlist_tracks_track
  ON playlist_tracks(track_id);

-- Step 3: Add comments for documentation
COMMENT ON TABLE playlist_tracks IS 'Track membership in playlists with ordering';
COMMENT ON COLUMN playlist_tracks.position IS 'Zero-based position of track in playlist';

COMMIT;

-- ============================================
-- DOWN MIGRATION
-- ============================================

BEGIN;
DROP TABLE IF EXISTS playlist_tracks;
COMMIT;
```

### Backfill Strategy

```markdown
## Backfill Plan: <Migration Name>

### Approach
- Batch size: 1000 rows per iteration
- Throttle: 100ms pause between batches
- Parallelism: 1 (sequential to avoid lock contention)
- Estimated duration: ~2 hours for 10M rows

### Script
\`\`\`sql
DO $$
DECLARE
  batch_size INT := 1000;
  affected INT;
BEGIN
  LOOP
    UPDATE playlists
    SET track_count = (
      SELECT COUNT(*) FROM playlist_tracks
      WHERE playlist_tracks.playlist_id = playlists.id
    )
    WHERE id IN (
      SELECT id FROM playlists
      WHERE track_count IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );

    GET DIAGNOSTICS affected = ROW_COUNT;
    EXIT WHEN affected = 0;

    RAISE NOTICE 'Updated % rows', affected;
    PERFORM pg_sleep(0.1);  -- throttle
  END LOOP;
END $$;
\`\`\`

### Validation
- Row count before: SELECT COUNT(*) WHERE track_count IS NULL
- Row count after: should be 0
- Spot check: Compare 100 random rows against COUNT(*) query
```

---

## Phase 4: Index Design

### Index Strategy

Design indexes based on access patterns (from Phase 1):

```markdown
## Index Design

### Primary Indexes (from PKs and unique constraints)
| Index | Type | Columns | Covers Pattern |
|-------|------|---------|---------------|
| PK playlist_tracks | B-tree | (id) | — |
| UQ playlist_track | B-tree | (playlist_id, track_id) | R5 |

### Secondary Indexes
| Index | Type | Columns | Covers Pattern | Justification |
|-------|------|---------|---------------|--------------|
| idx_pt_playlist_pos | B-tree | (playlist_id, position) | R1 | Ordered track list |
| idx_pt_track | B-tree | (track_id) | FK lookups | Cascade delete performance |
| idx_playlists_owner | B-tree | (owner_id, created_at DESC) | R2 | User's playlist list |
| idx_playlists_search | GIN | (to_tsvector(title)) | R3 | Full-text search |

### Composite Index Rules
- Column order: equality columns first, range/sort columns last
- Include columns for covering indexes (avoid table lookup)
- Partial indexes for filtered queries: `WHERE deleted_at IS NULL`

### Index Anti-Patterns to Avoid
- ❌ Index on every column (write overhead)
- ❌ Redundant indexes (A,B already covers queries on A alone)
- ❌ Index on low-cardinality columns (boolean, status with 3 values)
- ❌ Unused indexes (monitor with pg_stat_user_indexes)
```

### Query Plan Verification

```sql
-- Verify each access pattern uses the expected index
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM playlist_tracks
WHERE playlist_id = 'uuid-here'
ORDER BY position;

-- Expected: Index Scan using idx_pt_playlist_pos
-- Red flag: Seq Scan on large table
```

---

## Phase 5: Data Validation Rules

### Constraints

```sql
-- Table-level constraints
ALTER TABLE playlists
  ADD CONSTRAINT chk_playlists_title_length
    CHECK (LENGTH(title) BETWEEN 1 AND 200),
  ADD CONSTRAINT chk_playlists_description_length
    CHECK (description IS NULL OR LENGTH(description) <= 5000);

ALTER TABLE playlist_tracks
  ADD CONSTRAINT chk_playlist_tracks_position_range
    CHECK (position >= 0 AND position < 10000);

ALTER TABLE playlist_collaborators
  ADD CONSTRAINT chk_collaborator_role
    CHECK (role IN ('editor', 'viewer'));
```

### Triggers

Use triggers sparingly, only for cross-row validation or derived data:

```sql
-- Auto-update track_count on playlist_tracks changes
CREATE OR REPLACE FUNCTION update_playlist_track_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE playlists SET track_count = track_count + 1,
                         updated_at = NOW()
    WHERE id = NEW.playlist_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE playlists SET track_count = track_count - 1,
                         updated_at = NOW()
    WHERE id = OLD.playlist_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_playlist_track_count
  AFTER INSERT OR DELETE ON playlist_tracks
  FOR EACH ROW
  EXECUTE FUNCTION update_playlist_track_count();
```

### Application-Level Validation

Validate BEFORE hitting the database:

```markdown
| Field | Validation | DB Constraint | App Validation |
|-------|-----------|---------------|----------------|
| title | 1-200 chars, no only-whitespace | CHECK + NOT NULL | trim() + length check |
| position | 0 to track_count | CHECK >= 0 | Range validation |
| track_id | Must exist in tracks table | FK constraint | Pre-check query |
| role | 'editor' or 'viewer' | CHECK IN | Enum validation |
```

---

## Phase 6: Security

### Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE playlists ENABLE ROW LEVEL SECURITY;

-- Owner can do everything
CREATE POLICY playlists_owner ON playlists
  USING (owner_id = current_setting('app.current_user_id')::UUID);

-- Public playlists are readable by all
CREATE POLICY playlists_public_read ON playlists
  FOR SELECT
  USING (is_public = true);

-- Collaborators can read
CREATE POLICY playlists_collaborator_read ON playlists
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM playlist_collaborators
      WHERE playlist_id = playlists.id
        AND user_id = current_setting('app.current_user_id')::UUID
    )
  );
```

### Encryption at Rest

```markdown
## Encryption Requirements

| Column | Classification | Encryption |
|--------|---------------|-----------|
| playlist.title | Internal | Database-level TDE |
| playlist.description | Internal | Database-level TDE |
| user.email | Confidential | Application-level AES-256 |
| user.payment_info | Restricted | Vault (never in DB) |
```

### Audit Trail

```sql
-- Audit log table for sensitive operations
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  record_id UUID NOT NULL,
  action VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
  old_values JSONB,
  new_values JSONB,
  performed_by UUID NOT NULL,
  performed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ip_address INET
);

CREATE INDEX idx_audit_log_table_record
  ON audit_log(table_name, record_id, performed_at DESC);
```

---

## Phase 7: Testing

### Migration Tests

```markdown
## Migration Test Plan

### Up Migration Tests
| # | Test | SQL | Expected |
|---|------|-----|----------|
| 1 | Table created | \d playlist_tracks | Table exists with correct columns |
| 2 | Constraints active | INSERT invalid data | Constraint violation error |
| 3 | Indexes created | \di playlist_tracks* | All indexes present |
| 4 | FK cascades work | DELETE parent | Child rows deleted |
| 5 | Triggers fire | INSERT track | Playlist track_count incremented |

### Down Migration Tests
| # | Test | SQL | Expected |
|---|------|-----|----------|
| 1 | Table dropped | \d playlist_tracks | Table does not exist |
| 2 | No orphan references | Check FK tables | No broken references |

### Data Integrity Tests
| # | Test | Query | Expected |
|---|------|-------|----------|
| 1 | No orphan tracks | LEFT JOIN playlists WHERE NULL | 0 rows |
| 2 | Positions contiguous | Gaps in position sequence | 0 gaps |
| 3 | Track counts accurate | Compare count vs track_count | All match |
```

### Seed Data

```sql
-- Seed data for development and testing
-- Create test users
INSERT INTO users (id, username, email) VALUES
  ('11111111-1111-1111-1111-111111111111', 'test_user_1', 'test1@example.com'),
  ('22222222-2222-2222-2222-222222222222', 'test_user_2', 'test2@example.com');

-- Create test playlists (various states)
INSERT INTO playlists (id, owner_id, title, is_public, track_count) VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-...', 'Empty Playlist', true, 0),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-...', 'Full Playlist', true, 3),
  ('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-...', 'Private Playlist', false, 1),
  ('dddddddd-dddd-dddd-dddd-dddddddddddd', '22222222-...', 'Other User Playlist', true, 2);

-- Create test tracks in playlists
INSERT INTO playlist_tracks (playlist_id, track_id, position, added_by) VALUES
  ('bbbbbbbb-...', 'track-1', 0, '11111111-...'),
  ('bbbbbbbb-...', 'track-2', 1, '11111111-...'),
  ('bbbbbbbb-...', 'track-3', 2, '11111111-...');
```

### Load Testing Queries

```markdown
## Performance Benchmarks

Run these against production-like data volumes:

| Query Pattern | Target Rows | Target Latency | Query |
|-------------|-------------|---------------|-------|
| R1: Playlist with tracks | 5B tracks | < 50ms | SELECT ... WHERE playlist_id = ? ORDER BY position LIMIT 50 |
| R2: User playlists | 500M playlists | < 100ms | SELECT ... WHERE owner_id = ? ORDER BY created_at DESC LIMIT 20 |
| R3: Search | 500M playlists | < 200ms | SELECT ... WHERE to_tsvector(title) @@ to_tsquery(?) LIMIT 20 |
| W2: Add track | 5B tracks | < 100ms | INSERT INTO playlist_tracks ... |
| W3: Reorder | 10K tracks/playlist | < 200ms | UPDATE playlist_tracks SET position = ... WHERE playlist_id = ? |
```

---

## Phase 8: Documentation

### ERD Template

```markdown
## Entity Relationship Diagram

\`\`\`mermaid
erDiagram
    USERS ||--o{ PLAYLISTS : owns
    USERS ||--o{ PLAYLIST_COLLABORATORS : collaborates
    PLAYLISTS ||--o{ PLAYLIST_TRACKS : contains
    PLAYLISTS ||--o{ PLAYLIST_COLLABORATORS : has
    TRACKS ||--o{ PLAYLIST_TRACKS : "included in"

    USERS {
        uuid id PK
        varchar username
        varchar email
        timestamptz created_at
    }

    PLAYLISTS {
        uuid id PK
        uuid owner_id FK
        varchar title
        text description
        boolean is_public
        integer track_count
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    PLAYLIST_TRACKS {
        uuid id PK
        uuid playlist_id FK
        uuid track_id FK
        integer position
        uuid added_by FK
        timestamptz added_at
    }

    PLAYLIST_COLLABORATORS {
        uuid id PK
        uuid playlist_id FK
        uuid user_id FK
        varchar role
        timestamptz invited_at
    }
\`\`\`
```

### Data Dictionary Template

```markdown
## Data Dictionary

### Table: playlists

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | UUID | NO | gen_random_uuid() | Primary key |
| owner_id | UUID | NO | — | FK to users.id, playlist creator |
| title | VARCHAR(200) | NO | — | Display name, 1-200 chars |
| description | TEXT | YES | NULL | Optional description, max 5000 chars |
| is_public | BOOLEAN | NO | false | Whether visible to non-owner users |
| track_count | INTEGER | NO | 0 | Denormalized count, maintained by trigger |
| created_at | TIMESTAMPTZ | NO | NOW() | Record creation time |
| updated_at | TIMESTAMPTZ | NO | NOW() | Last modification time |
| deleted_at | TIMESTAMPTZ | YES | NULL | Soft delete timestamp, NULL if active |

### Indexes
| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| playlists_pkey | (id) | B-tree, unique | Primary key |
| idx_playlists_owner | (owner_id, created_at DESC) | B-tree | User's playlist list |
| idx_playlists_search | (to_tsvector('english', title)) | GIN | Full-text search |

### Constraints
| Name | Type | Definition |
|------|------|-----------|
| chk_playlists_title_length | CHECK | LENGTH(title) BETWEEN 1 AND 200 |
| chk_playlists_description_length | CHECK | description IS NULL OR LENGTH(description) <= 5000 |
| fk_playlists_owner | FK | owner_id REFERENCES users(id) |

### RLS Policies
| Policy | Operation | Rule |
|--------|----------|------|
| playlists_owner | ALL | owner_id = current_user |
| playlists_public_read | SELECT | is_public = true |
| playlists_collaborator_read | SELECT | EXISTS in collaborators |
```

## Output Checklist

When designing a new schema, produce:

1. ✅ **Entity Analysis**: All entities, relationships, lifecycle
2. ✅ **Access Patterns**: All read/write/aggregation queries with SLAs
3. ✅ **Schema DDL**: Complete CREATE TABLE statements
4. ✅ **Normalization Rationale**: Why each denormalization was chosen
5. ✅ **Migration Files**: Up + Down with backfill scripts
6. ✅ **Index Design**: Covering all access patterns
7. ✅ **Validation Rules**: Constraints + triggers + app-level
8. ✅ **Security Config**: RLS policies + encryption decisions
9. ✅ **Test Plan**: Migration tests + seed data + load tests
10. ✅ **ERD Diagram**: Mermaid ERD
11. ✅ **Data Dictionary**: Every table, column, index, constraint
