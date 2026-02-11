#!/usr/bin/env python3
"""
Pigment audit change inspector.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - fallback for older Python
    ZoneInfo = None  # type: ignore

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-"
    r"[0-9a-fA-F]{12}"
)


@dataclass
class MetadataContext:
    index: Dict[str, Dict[str, Any]]
    dependency_method: Dict[str, str]
    reverse_deps: Dict[str, List[str]]
    views_using: Dict[str, int]
    boards_using: Dict[str, int]


@dataclass
class DiffContext:
    diff_changed_fields: Dict[str, str]
    diff_summary: Dict[str, str]


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
    )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect Pigment audit logs for changes and blast radius."
    )
    parser.add_argument("--audit", required=False, help="Path to audit CSV export")
    parser.add_argument("--metadata", help="Path to metadata snapshot (file or directory)")
    parser.add_argument("--metadata-before", help="Path to metadata BEFORE snapshot")
    parser.add_argument("--metadata-after", help="Path to metadata AFTER snapshot")
    parser.add_argument("--out", default="./out", help="Output directory")
    parser.add_argument("--from", dest="date_from", help="Start date YYYY-MM-DD")
    parser.add_argument("--to", dest="date_to", help="End date YYYY-MM-DD")
    parser.add_argument("--app-id", action="append", default=[], help="Filter by application id")
    parser.add_argument("--app-name", action="append", default=[], help="Filter by application name substring")
    parser.add_argument("--user-email", action="append", default=[], help="Filter by user email substring")
    parser.add_argument("--event-type", action="append", default=[], help="Filter by event type")
    parser.add_argument("--include-access", action="store_true", help="Include access events in outputs")
    parser.add_argument("--only-changes", action="store_true", help="Keep only change/auth/export events (default)")
    parser.add_argument("--all-events", action="store_true", help="Do not filter out any events")
    parser.add_argument("--timezone", default="UTC", help="Timezone for report display")
    parser.add_argument("--top", type=int, default=20, help="Top N items in report sections")
    parser.add_argument("--format", choices=["csv", "parquet"], default="csv", help="Output format for tables")
    parser.add_argument("--chunk-rows", type=int, default=None, help="CSV chunk size (rows)")
    parser.add_argument("--smoke-test", action="store_true", help="Run a tiny in-memory self-test")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    return parser.parse_args(argv)


def safe_str(val: Any) -> Optional[str]:
    if val is None:
        return None
    if isinstance(val, float) and pd.isna(val):
        return None
    s = str(val)
    return s if s.strip() != "" else None


def parse_timestamp_series(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=True)


def iso_format_series(series: pd.Series) -> pd.Series:
    return series.dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_payload(val: Any) -> Tuple[Dict[str, Any], bool]:
    if val is None:
        return {}, False
    if isinstance(val, float) and pd.isna(val):
        return {}, False
    s = str(val).strip()
    if not s:
        return {}, False
    try:
        return json.loads(s), False
    except Exception:
        return {}, True


def get_nested(obj: Dict[str, Any], path: List[str]) -> Any:
    cur: Any = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur.get(key)
        else:
            return None
    return cur


def flatten_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "payload_entity_application_id": get_nested(payload, ["entity", "application", "id"]),
        "payload_entity_application_name": get_nested(payload, ["entity", "application", "name"]),
        "payload_entity_type": get_nested(payload, ["entity", "entityType"]),
        "payload_entity_id": get_nested(payload, ["entity", "id"]),
        "payload_entity_name": get_nested(payload, ["entity", "name"]),
        "payload_settings_dataType": get_nested(payload, ["settings", "dataType"]),
        "payload_settings_isSecurityBlock": get_nested(payload, ["settings", "isSecurityBlock"]),
        "payload_type": payload.get("type"),
    }


def normalize_actor_label(actor_type: Any) -> str:
    try:
        val = int(actor_type)
    except Exception:
        return "unknown"
    if val == 1:
        return "user"
    if val == 2:
        return "service"
    return "unknown"


def categorize_event(event_type: Optional[str]) -> str:
    if not event_type:
        return "other"
    t = event_type.lower()
    if "accessed" in t:
        return "access"
    if "login" in t or "impersonation" in t:
        return "auth"
    if "export" in t:
        return "export"
    if any(k in t for k in ["created", "updated", "deleted", "datachanged", "security", "permission", "accessright", "formula", "role", "rights"]):
        return "change"
    return "other"


def is_change_event(event_type: Optional[str]) -> bool:
    if not event_type:
        return False
    t = event_type.lower()
    return any(k in t for k in ["created", "updated", "deleted", "datachanged", "security", "permission", "accessright", "formula", "role", "rights"])


def base_severity(event_type: Optional[str]) -> str:
    if not event_type:
        return "LOW"
    t = event_type.lower()
    if any(k in t for k in ["impersonation", "permission", "accessright", "security", "deleted"]):
        return "CRITICAL"
    if any(k in t for k in ["metricupdated", "metriccreated", "metricdeleted", "dimensionupdated", "dimensioncreated", "dimensiondeleted", "formula", "boardupdated", "boardcreated", "viewupdated", "viewcreated", "tableupdated", "tablecreated"]):
        return "HIGH"
    if any(k in t for k in ["datachanged", "export"]):
        return "MEDIUM"
    if "accessed" in t or "login" in t:
        return "LOW"
    if is_change_event(event_type):
        return "MEDIUM"
    return "LOW"


def compute_risk(
    event_type: Optional[str],
    severity: str,
    meta: Dict[str, Any],
) -> Tuple[int, str]:
    base_scores = {"CRITICAL": 80, "HIGH": 60, "MEDIUM": 40, "LOW": 10}
    score = base_scores.get(severity, 10)
    reasons: List[str] = []
    et = (event_type or "").lower()

    if "deleted" in et:
        score += 10
        reasons.append("deletion")
    if "formula" in et:
        score += 8
        reasons.append("formula_change")
    if "metric" in et and "updated" in et:
        score += 6
        reasons.append("metric_update")
    if "export" in et:
        reasons.append("data_export")
    if "impersonation" in et:
        reasons.append("impersonation")

    if meta.get("is_security_block") is True:
        score += 15
        reasons.append("security_block")

    data_type = safe_str(meta.get("data_type")) or ""
    if data_type and any(k in data_type.lower() for k in ["number", "currency", "percentage", "rate", "kpi"]):
        score += 5
        reasons.append("fundamental_data_type")

    direct = meta.get("direct_dependents_count")
    transitive = meta.get("transitive_dependents_count")
    boards = meta.get("boards_using_count")
    views = meta.get("views_using_count")

    if isinstance(direct, int) and direct > 0:
        score += min(20, direct * 2)
        reasons.append(f"direct_dependents={direct}")
    if isinstance(transitive, int) and transitive > 0:
        score += min(20, transitive)
        reasons.append(f"transitive_dependents={transitive}")
    if isinstance(boards, int) and boards > 0:
        score += min(15, boards * 3)
        reasons.append(f"boards_using={boards}")
    if isinstance(views, int) and views > 0:
        score += min(10, views)
        reasons.append(f"views_using={views}")

    score = max(0, min(100, score))
    return score, ";".join(reasons)


def process_chunk(df: pd.DataFrame, row_offset: int) -> pd.DataFrame:
    df = df.copy()
    for col in [
        "event_id",
        "event_timestamp",
        "event_type",
        "payload_json",
        "actor_type",
        "entity_application_id",
        "entity_application_name",
        "entity_id",
        "entity_name",
        "entity_type",
        "user_email",
        "organization_name",
    ]:
        if col not in df.columns:
            df[col] = None
    df["__row_num"] = range(row_offset, row_offset + len(df))
    df["event_id"] = df["event_id"].astype(str)
    missing = df["event_id"].isna() | (df["event_id"].str.strip() == "") | (df["event_id"].str.lower() == "nan")
    df.loc[missing, "event_id"] = df.loc[missing, "__row_num"].map(lambda i: f"missing:{i}")

    df["event_timestamp_utc"] = parse_timestamp_series(df.get("event_timestamp"))
    df["event_timestamp_iso"] = iso_format_series(df["event_timestamp_utc"])

    payloads: List[Dict[str, Any]] = []
    parse_errors: List[bool] = []
    for val in df.get("payload_json", pd.Series([None] * len(df))):
        payload, err = parse_payload(val)
        payloads.append(payload)
        parse_errors.append(err)
    df["payload_parse_error"] = parse_errors

    payload_flat = [flatten_payload(p) for p in payloads]
    payload_df = pd.DataFrame(payload_flat)
    df = pd.concat([df.reset_index(drop=True), payload_df.reset_index(drop=True)], axis=1)

    actor_series = df["actor_type"] if "actor_type" in df.columns else pd.Series([None] * len(df))
    df["actor_label"] = actor_series.map(normalize_actor_label)

    df["application_id"] = df["payload_entity_application_id"].fillna(df.get("entity_application_id"))
    df["application_name"] = df["payload_entity_application_name"].fillna(df.get("entity_application_name"))

    event_series = df["event_type"] if "event_type" in df.columns else pd.Series([None] * len(df))
    df["category"] = event_series.map(categorize_event)
    df["is_change_event"] = event_series.map(is_change_event)
    df["severity"] = event_series.map(base_severity)

    return df


def dedupe_events(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by=["event_timestamp_utc", "event_id"], kind="mergesort")
    df = df.drop_duplicates(subset=["event_id"], keep="last")
    return df


def read_audit_csv(path: str, chunk_rows: Optional[int] = None) -> pd.DataFrame:
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if chunk_rows is None and size_mb > 50:
        chunk_rows = 200_000

    if chunk_rows:
        logging.info("Reading audit CSV in chunks of %s rows", chunk_rows)
        store: Dict[str, Dict[str, Any]] = {}
        offset = 0
        for chunk in pd.read_csv(path, dtype=str, chunksize=chunk_rows, low_memory=False):
            processed = process_chunk(chunk, offset)
            processed = processed.sort_values(by=["event_timestamp_utc", "event_id"], kind="mergesort")
            processed = processed.drop_duplicates(subset=["event_id"], keep="last")
            for _, row in processed.iterrows():
                eid = row.get("event_id")
                if eid is None:
                    continue
                ts = row.get("event_timestamp_utc")
                existing = store.get(eid)
                if existing is None:
                    store[eid] = row.to_dict()
                else:
                    existing_ts = existing.get("event_timestamp_utc")
                    if pd.isna(existing_ts) or (pd.notna(ts) and ts > existing_ts):
                        store[eid] = row.to_dict()
            offset += len(chunk)
        df = pd.DataFrame(store.values())
        return dedupe_events(df)

    logging.info("Reading audit CSV")
    df = pd.read_csv(path, dtype=str, low_memory=False)
    df = process_chunk(df, 0)
    return dedupe_events(df)


def normalize_collection_name(name: str) -> str:
    n = name.lower()
    if n in {"app", "apps", "applications", "application"}:
        return "applications"
    if n in {"blocks", "block"}:
        return "blocks"
    if n in {"boards", "board"}:
        return "boards"
    if n in {"views", "view"}:
        return "views"
    if n in {"org", "orgs", "organization", "organizations"}:
        return "orgs"
    if n in {"metrics", "metric"}:
        return "metrics"
    if n in {"lists", "list"}:
        return "lists"
    if n in {"dimensions", "dimension"}:
        return "dimensions"
    if n in {"tables", "table"}:
        return "tables"
    return n


def load_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata(path: str) -> Dict[str, List[Dict[str, Any]]]:
    collections: Dict[str, List[Dict[str, Any]]] = {}
    if os.path.isdir(path):
        for fname in os.listdir(path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(path, fname)
            try:
                data = load_json_file(fpath)
            except Exception as exc:
                logging.warning("Failed to parse %s: %s", fpath, exc)
                continue
            key = normalize_collection_name(os.path.splitext(fname)[0])
            if isinstance(data, list):
                collections[key] = data
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        collections[normalize_collection_name(k)] = v
    else:
        data = load_json_file(path)
        if isinstance(data, list):
            collections["items"] = data
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    collections[normalize_collection_name(k)] = v
    return collections


def first_present(item: Dict[str, Any], keys: Iterable[str]) -> Any:
    for k in keys:
        if k in item and item[k] is not None:
            return item[k]
    return None


def normalize_list_of_ids(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out = []
        for v in value:
            if isinstance(v, dict):
                vid = first_present(v, ["id", "uuid", "entityId", "blockId", "viewId", "boardId"])
                if vid:
                    out.append(str(vid))
            else:
                out.append(str(v))
        return [x for x in out if x]
    if isinstance(value, dict):
        vid = first_present(value, ["id", "uuid", "entityId", "blockId", "viewId", "boardId"])
        return [str(vid)] if vid else []
    return [str(value)]


def normalize_entity(item: Dict[str, Any], collection_hint: str) -> Optional[Dict[str, Any]]:
    entity_id = first_present(item, ["id", "uuid", "uid", "entityId", "blockId", "viewId", "boardId", "metricId", "listId"])
    if not entity_id:
        return None

    name = first_present(item, ["name", "friendlyName", "title", "displayName"])
    raw_type = first_present(item, ["entityType", "blockType", "type"])

    data_type = None
    entity_type = None
    if isinstance(raw_type, str):
        if raw_type.startswith("BlockDataType_"):
            data_type = raw_type
        elif raw_type.lower() in {"number", "currency", "text", "date", "boolean", "percentage"}:
            data_type = raw_type
        else:
            entity_type = raw_type
    hint_type = collection_hint.rstrip("s").capitalize()
    entity_type = entity_type or hint_type

    application_id = first_present(item, ["applicationId", "application_id", "appId", "app_id"])
    application_name = first_present(item, ["applicationName", "application_name"])
    if isinstance(item.get("application"), dict):
        application_id = application_id or item["application"].get("id")
        application_name = application_name or item["application"].get("name")

    is_security_block = first_present(item, ["isSecurityBlock", "isSecurity", "securityBlock"])
    if isinstance(is_security_block, str):
        is_security_block = is_security_block.lower() == "true"

    dimensions = normalize_list_of_ids(first_present(item, ["dimensions", "dimensionIds", "dimension_ids", "listDimensions", "dimensionListIds"]))
    formula = first_present(item, ["formula", "expression", "rawFormula", "formulaString"])
    explicit_deps = normalize_list_of_ids(first_present(item, ["referencedBlocks", "referencedBlockIds", "dependencies", "dependencyIds", "blockDependencies"]))

    if not data_type:
        data_type = first_present(item, ["dataType", "blockDataType"])

    return {
        "id": str(entity_id),
        "name": name,
        "entity_type": entity_type,
        "application_id": application_id,
        "application_name": application_name,
        "data_type": data_type,
        "is_security_block": is_security_block,
        "dimensions": dimensions,
        "formula": formula,
        "explicit_dependencies": explicit_deps,
        "raw": item,
    }


def extract_uuid_dependencies(formula: Any) -> List[str]:
    if not formula:
        return []
    s = str(formula)
    return list({m.group(0) for m in UUID_RE.finditer(s)})


def build_metadata_context(collections: Dict[str, List[Dict[str, Any]]]) -> MetadataContext:
    index: Dict[str, Dict[str, Any]] = {}
    views_raw: List[Tuple[str, Dict[str, Any]]] = []
    boards_raw: List[Tuple[str, Dict[str, Any]]] = []

    for name, items in collections.items():
        hint = normalize_collection_name(name)
        for item in items:
            if not isinstance(item, dict):
                continue
            norm = normalize_entity(item, hint)
            if not norm:
                continue
            entity_id = norm["id"]
            index[entity_id] = norm
            if norm["entity_type"].lower() == "view" or hint == "views":
                views_raw.append((entity_id, item))
            if norm["entity_type"].lower() == "board" or hint == "boards":
                boards_raw.append((entity_id, item))

    dependency_method: Dict[str, str] = {}
    deps_map: Dict[str, List[str]] = {}

    for entity_id, norm in index.items():
        explicit = norm.get("explicit_dependencies") or []
        if explicit:
            deps_map[entity_id] = [d for d in explicit if d in index]
            dependency_method[entity_id] = "explicit"
        else:
            deps_map[entity_id] = []

    for entity_id, norm in index.items():
        if deps_map.get(entity_id):
            continue
        formula = norm.get("formula")
        ids = [d for d in extract_uuid_dependencies(formula) if d in index]
        if ids:
            deps_map[entity_id] = ids
            dependency_method[entity_id] = "regex"
        else:
            dependency_method[entity_id] = "none"

    reverse_deps: Dict[str, List[str]] = {}
    for src, deps in deps_map.items():
        for dep in deps:
            reverse_deps.setdefault(dep, []).append(src)

    view_underlying: Dict[str, str] = {}
    for view_id, view in views_raw:
        underlying_id = first_present(view, ["underlyingId", "underlyingBlockId", "blockId", "contentId"])
        if underlying_id:
            view_underlying[view_id] = str(underlying_id)

    views_using: Dict[str, int] = {}
    for view_id, underlying_id in view_underlying.items():
        views_using[underlying_id] = views_using.get(underlying_id, 0) + 1

    boards_using: Dict[str, int] = {}
    for board_id, board in boards_raw:
        blocks = board.get("blocks") or board.get("boardBlocks") or []
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_id = first_present(block, ["blockId", "id", "contentId"])
            block_type = (first_present(block, ["blockType", "type"]) or "").lower()
            if not block_id:
                continue
            block_id = str(block_id)
            if block_type == "view" and block_id in view_underlying:
                target = view_underlying[block_id]
            else:
                target = block_id
            boards_using[target] = boards_using.get(target, 0) + 1

    return MetadataContext(
        index=index,
        dependency_method=dependency_method,
        reverse_deps=reverse_deps,
        views_using=views_using,
        boards_using=boards_using,
    )


def compute_transitive_dependents(
    entity_id: str,
    reverse_deps: Dict[str, List[str]],
    max_nodes: int = 5000,
    max_depth: int = 6,
) -> int:
    visited = set()
    queue: List[Tuple[str, int]] = [(entity_id, 0)]
    while queue and len(visited) < max_nodes:
        current, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for dep in reverse_deps.get(current, []):
            if dep in visited:
                continue
            visited.add(dep)
            queue.append((dep, depth + 1))
    if entity_id in visited:
        visited.remove(entity_id)
    return len(visited)


def build_diff_context(
    before: Optional[MetadataContext],
    after: Optional[MetadataContext],
) -> DiffContext:
    if not before or not after:
        return DiffContext(diff_changed_fields={}, diff_summary={})
    changed_fields: Dict[str, str] = {}
    diff_summary: Dict[str, str] = {}
    keys = [
        "name",
        "entity_type",
        "application_id",
        "application_name",
        "data_type",
        "is_security_block",
        "dimensions",
        "formula",
        "explicit_dependencies",
    ]
    all_ids = set(before.index.keys()) | set(after.index.keys())
    for entity_id in all_ids:
        before_item = before.index.get(entity_id, {})
        after_item = after.index.get(entity_id, {})
        diffs = []
        summaries = []
        for key in keys:
            b = before_item.get(key)
            a = after_item.get(key)
            if b != a:
                diffs.append(key)
                b_str = str(b)[:120] if b is not None else "None"
                a_str = str(a)[:120] if a is not None else "None"
                summaries.append(f"{key}: {b_str} -> {a_str}")
        if diffs:
            changed_fields[entity_id] = ",".join(diffs)
            diff_summary[entity_id] = "; ".join(summaries)
    return DiffContext(diff_changed_fields=changed_fields, diff_summary=diff_summary)


def apply_filters(df: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    df = df.copy()
    if args.date_from:
        start = pd.to_datetime(args.date_from, utc=True)
        df = df[df["event_timestamp_utc"] >= start]
    if args.date_to:
        end = pd.to_datetime(args.date_to, utc=True) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        df = df[df["event_timestamp_utc"] <= end]

    if args.app_id:
        df = df[df["application_id"].isin(args.app_id)]
    if args.app_name:
        mask = False
        for name in args.app_name:
            mask |= df["application_name"].str.contains(name, case=False, na=False)
        df = df[mask]
    if args.user_email:
        mask = False
        for email in args.user_email:
            mask |= df["user_email"].str.contains(email, case=False, na=False)
        df = df[mask]
    if args.event_type:
        df = df[df["event_type"].isin(args.event_type)]

    if args.all_events:
        return df

    allowed = {"change", "auth", "export"}
    if args.include_access:
        allowed.add("access")
    df = df[df["category"].isin(allowed)]
    return df


def enrich_with_metadata(
    df: pd.DataFrame,
    meta: Optional[MetadataContext],
    diff: Optional[DiffContext],
) -> pd.DataFrame:
    df = df.copy()
    if not meta:
        df["meta_name"] = None
        df["meta_entity_type"] = None
        df["meta_application_id"] = None
        df["meta_application_name"] = None
        df["meta_data_type"] = None
        df["meta_is_security_block"] = None
        df["meta_dimensions"] = None
        df["dependency_extraction_method"] = None
        df["direct_dependents_count"] = None
        df["transitive_dependents_count"] = None
        df["boards_using_count"] = None
        df["views_using_count"] = None
    else:
        cache_transitive: Dict[str, int] = {}

        def lookup(entity_id: Any) -> Dict[str, Any]:
            if entity_id is None or (isinstance(entity_id, float) and pd.isna(entity_id)):
                return {}
            return meta.index.get(str(entity_id), {})

        def direct_count(entity_id: Any) -> Optional[int]:
            if entity_id is None or (isinstance(entity_id, float) and pd.isna(entity_id)):
                return None
            return len(meta.reverse_deps.get(str(entity_id), []))

        def transitive_count(entity_id: Any) -> Optional[int]:
            if entity_id is None or (isinstance(entity_id, float) and pd.isna(entity_id)):
                return None
            key = str(entity_id)
            if key in cache_transitive:
                return cache_transitive[key]
            count = compute_transitive_dependents(key, meta.reverse_deps)
            cache_transitive[key] = count
            return count

        df["meta_name"] = df["entity_id"].map(lambda x: lookup(x).get("name"))
        df["meta_entity_type"] = df["entity_id"].map(lambda x: lookup(x).get("entity_type"))
        df["meta_application_id"] = df["entity_id"].map(lambda x: lookup(x).get("application_id"))
        df["meta_application_name"] = df["entity_id"].map(lambda x: lookup(x).get("application_name"))
        df["meta_data_type"] = df["entity_id"].map(lambda x: lookup(x).get("data_type"))
        df["meta_is_security_block"] = df["entity_id"].map(lambda x: lookup(x).get("is_security_block"))
        df["meta_dimensions"] = df["entity_id"].map(lambda x: lookup(x).get("dimensions"))
        df["dependency_extraction_method"] = df["entity_id"].map(lambda x: meta.dependency_method.get(str(x)))
        df["direct_dependents_count"] = df["entity_id"].map(direct_count)
        df["transitive_dependents_count"] = df["entity_id"].map(transitive_count)
        df["boards_using_count"] = df["entity_id"].map(lambda x: meta.boards_using.get(str(x)))
        df["views_using_count"] = df["entity_id"].map(lambda x: meta.views_using.get(str(x)))

    if diff:
        df["diff_changed_fields"] = df["entity_id"].map(lambda x: diff.diff_changed_fields.get(str(x)))
        df["diff_summary"] = df["entity_id"].map(lambda x: diff.diff_summary.get(str(x)))
    else:
        df["diff_changed_fields"] = None
        df["diff_summary"] = None

    def row_risk(row: pd.Series) -> Tuple[int, str]:
        meta_info = {
            "is_security_block": row.get("meta_is_security_block"),
            "data_type": row.get("meta_data_type"),
            "direct_dependents_count": row.get("direct_dependents_count"),
            "transitive_dependents_count": row.get("transitive_dependents_count"),
            "boards_using_count": row.get("boards_using_count"),
            "views_using_count": row.get("views_using_count"),
        }
        return compute_risk(row.get("event_type"), row.get("severity"), meta_info)

    risk = df.apply(row_risk, axis=1, result_type="expand")
    df["risk_score"] = risk[0]
    df["risk_reasons"] = risk[1]

    return df


def build_changes_timeline(df: pd.DataFrame) -> pd.DataFrame:
    changes = df[df["is_change_event"] == True].copy()  # noqa: E712
    changes = changes.sort_values(by=["event_timestamp_utc", "event_id"], kind="mergesort")
    return changes


def build_entity_summary(df: pd.DataFrame) -> pd.DataFrame:
    changes = df[df["is_change_event"] == True].copy()  # noqa: E712
    if changes.empty:
        return pd.DataFrame()

    changes["application_id_norm"] = changes["application_id"].fillna("unknown")
    changes["entity_type_norm"] = changes["entity_type"].fillna(changes["meta_entity_type"]).fillna("unknown")
    changes["entity_id_norm"] = changes["entity_id"].fillna("unknown")

    def agg_event_types(series: pd.Series) -> str:
        counts = series.value_counts()
        return ";".join([f"{k}={v}" for k, v in counts.items()])

    def agg_top_users(series: pd.Series) -> str:
        counts = series.value_counts()
        return ";".join([f"{k}={v}" for k, v in counts.head(5).items()])

    def severity_rank(val: Any) -> int:
        order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        return order.get(str(val), 0)

    grouped = changes.groupby(["application_id_norm", "entity_type_norm", "entity_id_norm"], dropna=False)
    summary = grouped.agg(
        application_name=("application_name", "first"),
        entity_name=("entity_name", "first"),
        meta_name=("meta_name", "first"),
        first_seen=("event_timestamp_utc", "min"),
        last_seen=("event_timestamp_utc", "max"),
        event_types=("event_type", agg_event_types),
        top_users=("user_email", agg_top_users),
        highest_severity=("severity", lambda s: max(s, key=severity_rank)),
        max_risk_score=("risk_score", "max"),
        direct_dependents_count=("direct_dependents_count", "max"),
        transitive_dependents_count=("transitive_dependents_count", "max"),
        boards_using_count=("boards_using_count", "max"),
        views_using_count=("views_using_count", "max"),
    ).reset_index()

    return summary


def format_dt_for_report(ts: Optional[pd.Timestamp], tz: str) -> str:
    if ts is None or pd.isna(ts):
        return "unknown"
    if ZoneInfo is None:
        return ts.strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        tzinfo = ZoneInfo(tz)
    except Exception:
        tzinfo = ZoneInfo("UTC")
    return ts.tz_convert(tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z")


def build_report(df: pd.DataFrame, changes: pd.DataFrame, out_dir: str, tz: str, top_n: int) -> None:
    total_events = len(df)
    total_changes = len(changes)
    orgs = sorted({x for x in df.get("organization_name", pd.Series()).dropna().unique()})
    apps = sorted({x for x in df.get("application_name", pd.Series()).dropna().unique()})
    start = df["event_timestamp_utc"].min()
    end = df["event_timestamp_utc"].max()

    report_lines: List[str] = []
    report_lines.append("# Pigment Audit Change Report")
    report_lines.append("")
    report_lines.append("## Executive Summary")
    summary_lines: List[str] = []
    summary_lines.append(
        f"- Period analyzed: {format_dt_for_report(start, tz)} to {format_dt_for_report(end, tz)}; "
        f"{total_events} events, {total_changes} changes."
    )

    if not changes.empty:
        top_change = changes.sort_values(
            by=["risk_score", "event_timestamp_utc"], ascending=[False, False]
        ).iloc[0]
        entity_label = top_change.get("entity_name") or top_change.get("meta_name") or "unknown"
        app_label = top_change.get("application_name") or "unknown"
        when = format_dt_for_report(top_change.get("event_timestamp_utc"), tz)
        summary_lines.append(
            f"- Top risk event: {top_change.get('event_type')} on {entity_label} "
            f"({app_label}) at {when}, risk={top_change.get('risk_score')}."
        )

        app_counts = (
            changes.groupby("application_name")["event_id"]
            .count()
            .sort_values(ascending=False)
            .head(2)
        )
        if not app_counts.empty:
            summary_lines.append(
                "- Most active apps: "
                + ", ".join([f"{idx} ({val})" for idx, val in app_counts.items()])
                + "."
            )

        user_counts = (
            changes.groupby("user_email")["event_id"]
            .count()
            .sort_values(ascending=False)
            .head(2)
        )
        if not user_counts.empty:
            summary_lines.append(
                "- Most active users: "
                + ", ".join([f"{idx or 'unknown'} ({val})" for idx, val in user_counts.items()])
                + "."
            )
    else:
        summary_lines.append("- No change events detected in the selected window.")

    export_count = int((df["category"] == "export").sum()) if "category" in df.columns else 0
    impersonation_count = int(
        df.get("event_type", pd.Series()).str.contains("Impersonation", case=False, na=False).sum()
    )
    summary_lines.append(
        f"- Sensitive activity: {export_count} exports, {impersonation_count} impersonation events."
    )

    report_lines.extend(summary_lines)
    report_lines.append("")
    report_lines.append("## Overview")
    report_lines.append(f"- Time range: {format_dt_for_report(start, tz)} to {format_dt_for_report(end, tz)}")
    report_lines.append(f"- Organizations: {', '.join(orgs) if orgs else 'unknown'}")
    report_lines.append(f"- Applications: {', '.join(apps) if apps else 'unknown'}")
    report_lines.append(f"- Total events: {total_events}")
    report_lines.append(f"- Total change events: {total_changes}")

    report_lines.append("")
    report_lines.append("## Top Changes (by risk score)")
    if changes.empty:
        report_lines.append("- No change events found.")
    else:
        top_changes = changes.sort_values(by=["risk_score", "event_timestamp_utc"], ascending=[False, False]).head(top_n)
        for _, row in top_changes.iterrows():
            when = format_dt_for_report(row.get("event_timestamp_utc"), tz)
            report_lines.append(
                f"- {when} | {row.get('severity')} | {row.get('event_type')} | "
                f"{row.get('entity_name') or row.get('meta_name')} | "
                f"{row.get('application_name')} | {row.get('user_email') or row.get('actor_label')} | "
                f"risk={row.get('risk_score')} | {row.get('risk_reasons')}"
            )

    report_lines.append("")
    report_lines.append("## Changes by Application")
    if changes.empty:
        report_lines.append("- No change events found.")
    else:
        by_app = changes.groupby("application_name").agg(
            change_count=("event_id", "count"),
            max_risk=("risk_score", "max"),
        ).reset_index().sort_values(by=["max_risk", "change_count"], ascending=False).head(top_n)
        for _, row in by_app.iterrows():
            report_lines.append(
                f"- {row.get('application_name')}: changes={row.get('change_count')}, max_risk={row.get('max_risk')}"
            )

    report_lines.append("")
    report_lines.append("## Changes by User")
    if changes.empty:
        report_lines.append("- No change events found.")
    else:
        by_user = changes.groupby("user_email").agg(
            change_count=("event_id", "count"),
            max_risk=("risk_score", "max"),
        ).reset_index().sort_values(by=["max_risk", "change_count"], ascending=False).head(top_n)
        for _, row in by_user.iterrows():
            report_lines.append(
                f"- {row.get('user_email') or 'unknown'}: changes={row.get('change_count')}, max_risk={row.get('max_risk')}"
            )

    report_lines.append("")
    report_lines.append("## High-Risk Items")
    high_risk = changes[(changes["severity"] == "CRITICAL") | (changes["risk_score"] >= 80)]
    if high_risk.empty:
        report_lines.append("- No high-risk items detected.")
    else:
        for _, row in high_risk.sort_values(by=["risk_score"], ascending=False).head(top_n).iterrows():
            when = format_dt_for_report(row.get("event_timestamp_utc"), tz)
            report_lines.append(
                f"- {when} | {row.get('event_type')} | {row.get('entity_name') or row.get('meta_name')} | "
                f"{row.get('application_name')} | risk={row.get('risk_score')} | {row.get('risk_reasons')}"
            )

    report_lines.append("")
    report_lines.append("## Exports and Impersonations")
    exports = df[df["category"] == "export"]
    impersonations = df[df["event_type"].str.contains("Impersonation", case=False, na=False)]
    if exports.empty and impersonations.empty:
        report_lines.append("- None detected.")
    else:
        for _, row in exports.head(top_n).iterrows():
            when = format_dt_for_report(row.get("event_timestamp_utc"), tz)
            report_lines.append(
                f"- Export | {when} | {row.get('entity_name') or row.get('meta_name')} | {row.get('user_email')}"
            )
        for _, row in impersonations.head(top_n).iterrows():
            when = format_dt_for_report(row.get("event_timestamp_utc"), tz)
            report_lines.append(
                f"- Impersonation | {when} | {row.get('user_email') or row.get('actor_label')}"
            )

    report_lines.append("")
    report_lines.append("## Next Checks")
    report_lines.append("- Validate critical deletions and security changes for intent and approvals.")
    report_lines.append("- Review formula or metric updates with high blast radius for regressions.")
    report_lines.append("- Confirm data exports were authorized and expected.")
    report_lines.append("- Audit impersonation sessions for scope and duration.")

    report_path = os.path.join(out_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    try:
        from jinja2 import Template  # type: ignore

        html_template = Template(
            """
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Pigment Audit Change Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1, h2 { color: #2b2b2b; }
    ul { line-height: 1.4; }
    code { background: #f3f3f3; padding: 2px 4px; }
  </style>
</head>
<body>
  <h1>Pigment Audit Change Report</h1>
  <div>
    {{ body | safe }}
  </div>
</body>
</html>
"""
        )
        html_body = "".join([f"<p>{line}</p>" for line in report_lines])
        html_out = html_template.render(body=html_body)
        with open(os.path.join(out_dir, "report.html"), "w", encoding="utf-8") as f:
            f.write(html_out)
    except Exception:
        logging.info("jinja2 not available; skipping HTML report")


def write_df(df: pd.DataFrame, out_dir: str, name: str, fmt: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    if fmt == "parquet":
        try:
            import pyarrow  # noqa: F401
            path = os.path.join(out_dir, f"{name}.parquet")
            df.to_parquet(path, index=False)
            return path
        except Exception:
            logging.warning("pyarrow not available; falling back to CSV for %s", name)
    path = os.path.join(out_dir, f"{name}.csv")
    df.to_csv(path, index=False)
    return path


def run_smoke_test() -> int:
    logging.info("Running smoke test")
    sample_events = pd.DataFrame([
        {
            "event_id": "1",
            "event_timestamp": "2025-12-10 10:21:32.065 UTC",
            "event_type": "MetricUpdated",
            "organization_name": "Demo Org",
            "actor_type": "1",
            "user_email": "user@example.com",
            "entity_type": "Metric",
            "entity_id": "11111111-1111-1111-1111-111111111111",
            "entity_name": "Revenue",
            "entity_application_id": "app-1",
            "entity_application_name": "FP&A",
            "payload_json": json.dumps({"entity": {"application": {"id": "app-1", "name": "FP&A"}}}),
        },
        {
            "event_id": "2",
            "event_timestamp": "2025-12-10 12:00:00.000 UTC",
            "event_type": "DataExported",
            "organization_name": "Demo Org",
            "actor_type": "2",
            "user_email": None,
            "entity_type": "View",
            "entity_id": "22222222-2222-2222-2222-222222222222",
            "entity_name": "Revenue View",
            "entity_application_id": "app-1",
            "entity_application_name": "FP&A",
            "payload_json": "{}",
        },
    ])
    processed = process_chunk(sample_events, 0)
    processed = dedupe_events(processed)

    meta = {
        "metrics": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "Revenue",
                "applicationId": "app-1",
                "dataType": "Number",
                "isSecurityBlock": False,
            }
        ],
        "views": [
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "Revenue View",
                "underlyingId": "11111111-1111-1111-1111-111111111111",
            }
        ],
    }
    meta_ctx = build_metadata_context(meta)
    diff_ctx = build_diff_context(None, None)
    enriched = enrich_with_metadata(processed, meta_ctx, diff_ctx)
    changes = build_changes_timeline(enriched)

    out_dir = "./out_smoke"
    write_df(enriched, out_dir, "events_enriched", "csv")
    write_df(changes, out_dir, "changes_timeline", "csv")
    write_df(build_entity_summary(enriched), out_dir, "entity_change_summary", "csv")
    build_report(enriched, changes, out_dir, "UTC", 5)
    logging.info("Smoke test output written to %s", out_dir)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)

    if args.smoke_test:
        return run_smoke_test()

    if not args.audit:
        logging.error("--audit is required unless --smoke-test is used")
        return 2

    df = read_audit_csv(args.audit, args.chunk_rows)
    df = apply_filters(df, args)

    meta_ctx = None
    diff_ctx = None
    if args.metadata:
        collections = load_metadata(args.metadata)
        meta_ctx = build_metadata_context(collections)
    if args.metadata_before and args.metadata_after:
        before = build_metadata_context(load_metadata(args.metadata_before))
        after = build_metadata_context(load_metadata(args.metadata_after))
        diff_ctx = build_diff_context(before, after)
        if not meta_ctx:
            meta_ctx = after

    df = enrich_with_metadata(df, meta_ctx, diff_ctx)

    changes = build_changes_timeline(df)
    summary = build_entity_summary(df)

    df = df.sort_values(by=["event_timestamp_utc", "event_id"], kind="mergesort")

    write_df(df, args.out, "events_enriched", args.format)
    write_df(changes, args.out, "changes_timeline", args.format)
    write_df(summary, args.out, "entity_change_summary", args.format)
    build_report(df, changes, args.out, args.timezone, args.top)

    logging.info("Done. Outputs written to %s", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
