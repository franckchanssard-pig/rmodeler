# Pigment Audit Change Inspector

A production-ready CLI that helps Pigment admins/modelers answer **“what changed?”** using audit log CSV exports and optional metadata snapshots. It enriches audit events with application context, estimates blast radius, computes risk scores, and outputs both machine-readable tables and a human-friendly report.

## Features
- Dedupes audit events by `event_id` and normalizes timestamps to UTC.
- Robust parsing of `payload_json` (safe against invalid JSON).
- Event categorization (access/auth/export/change) and severity + risk scoring.
- Metadata enrichment with best-effort dependency graphs and blast radius estimates.
- Optional diffs when you provide before/after metadata snapshots.
- Outputs: `events_enriched`, `changes_timeline`, `entity_change_summary`, `report.md` (+ optional HTML).

## Inputs

### Audit log CSV (required)
Provide via `--audit /path/to/audit.csv`.

Expected columns (best effort; missing columns are tolerated):
- `event_id`, `event_timestamp`, `event_type`
- `organization_id`, `organization_name`
- `actor_type` (1=user, 2=service/api)
- `user_id`, `user_name`, `user_email`
- `entity_type`, `entity_id`, `entity_name`
- `entity_application_id`, `entity_application_name`
- `payload_json` (JSON string)

### Metadata snapshots (optional but recommended)
Provide either:
- `--metadata /path/to/metadata.json` (single snapshot)
- or `--metadata-before /path/to/before.json --metadata-after /path/to/after.json`

Accepted formats:
- A single JSON file with top-level keys like `applications`, `blocks`, `boards`, `views`, `orgs`, etc.
- Or a directory containing JSON files like `applications.json`, `blocks.json`, `boards.json`, `views.json`.

The loader maps common field names (`id`, `uuid`, `name`, `applicationId`, `dataType`, `formula`, `referencedBlockIds`, etc.) on a best-effort basis.

## Usage

```bash
python pigment_audit_change_inspector.py \
  --audit audit.csv \
  --metadata metadata.json \
  --from 2025-12-01 \
  --to 2025-12-31 \
  --out out
```

```bash
python pigment_audit_change_inspector.py \
  --audit audit.csv \
  --metadata-before before.json \
  --metadata-after after.json \
  --app-name "FP&A" \
  --top 30
```

Optional flags:
- `--include-access` to include access events (default focuses on change/auth/export)
- `--only-changes` to explicitly keep change/auth/export events (default behavior)
- `--all-events` to disable filtering
- `--format parquet` (requires `pyarrow`)
- `--timezone Europe/Paris` (for report display only)
- `--chunk-rows 200000` for large CSVs
- `--smoke-test` to run a built-in sample

## Outputs (default `./out`)
- `events_enriched.csv` (or `.parquet`): all deduped events with enrichment
- `changes_timeline.csv`: change events only, sorted by time
- `entity_change_summary.csv`: per-entity rollups (counts, top users, blast radius)
- `report.md`: investigation-style summary
- `report.html` (optional if `jinja2` is installed)

## Risk Score & Blast Radius (short + honest)
Risk score is a practical heuristic:
- Base severity is derived from event type (deletions and security changes are highest).
- Score increases for:
  - Security blocks
  - Widely referenced entities (direct + transitive dependents)
  - Many views/boards using the entity
  - Fundamental data types (Number/Currency)

Blast radius is estimated using metadata:
- If explicit dependencies exist (e.g., `referencedBlockIds`), use those.
- Otherwise, the tool attempts conservative UUID extraction from formulas.
- If no metadata is available, blast radius fields are left empty.

## Requirements
- Python 3.11+
- `pandas`

Optional:
- `jinja2` for HTML reports
- `pyarrow` for Parquet output

---

If you want help tuning event categories, severity rules, or metadata mapping, open an issue or adjust the heuristics directly in `pigment_audit_change_inspector.py`.
