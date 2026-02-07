#!/usr/bin/env python3
import os, json, urllib.request
from urllib.error import HTTPError

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise SystemExit("Set TOKEN env var to your Bearer token")

APP_ID = os.environ.get("APP_ID", "0538f210-83af-4474-9b03-812a0c15e1ce")
ORG_ID = os.environ.get("ORG_ID", "5371eb8c-30e7-48cc-91b2-4d1c4a389d79")
API_HOST = os.environ.get("API_HOST", "https://staging.pigment.app")
BASE_APP = f"{API_HOST}/api/workspace/{APP_ID}"
BASE_WS = f"{API_HOST}/api/workspace"

TARGET_LIST_NAMES = {
    "TI Employee",
    "TI Account",
    "TI Project",
    "TI Time Entry",
}
TARGET_VIEW_NAMES = {
    "TI Time Entry",
    "TI Projects",
    "TI Hours",
}
TARGET_BOARD_NAMES = {
    "Time Input",
    "Time Overview",
}
TARGET_METRIC_NAMES = {
    "TI Hours",
}


def request(method, path, payload=None, base="app"):
    if path.startswith("http"):
        url = path
    else:
        root = BASE_APP if base == "app" else BASE_WS
        url = root + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else None
    except HTTPError as e:
        body = e.read().decode("utf-8")
        raise SystemExit(f"HTTP {e.code} on {path}: {body}")


def list_lists():
    return request("GET", "/list/ListForApplication")[1] or []


def list_metrics():
    return request("GET", "/metric/ListForApplication")[1] or []


def list_boards():
    return request("GET", "/board/List")[1] or []


def list_views_on_block(block_id, block_type):
    path = f"/internals/view/ListViewsOnBlock?organizationId={ORG_ID}&blockType={block_type}&blockId={block_id}"
    return request("GET", path, base="workspace")[1] or []


def delete_board(board_id):
    request("DELETE", f"/board/Remove/{board_id}")


def delete_view(view_id):
    request("DELETE", f"/view/Remove/{view_id}")


def delete_metric(metric_id):
    request("DELETE", f"/metric/Remove/{metric_id}")


def delete_list(list_id):
    request("DELETE", f"/list/Remove/{list_id}")


def main():
    lists = list_lists()
    metrics = list_metrics()
    boards = list_boards()

    list_by_name = {l.get("friendlyName"): l for l in lists}
    metric_by_name = {m.get("friendlyName"): m for m in metrics}
    board_by_name = {b.get("name") or b.get("friendlyName"): b for b in boards}

    # Delete boards first (they reference views)
    deleted_boards = []
    for name in TARGET_BOARD_NAMES:
        board = board_by_name.get(name)
        if board:
            delete_board(board["id"])
            deleted_boards.append(board["id"])

    # Delete views linked to target lists and metrics
    deleted_views = []
    for name in TARGET_LIST_NAMES:
        lst = list_by_name.get(name)
        if not lst:
            continue
        for v in list_views_on_block(lst["id"], "List"):
            if v.get("friendlyName") in TARGET_VIEW_NAMES or v.get("friendlyName", "").startswith("TI "):
                delete_view(v["id"])
                deleted_views.append(v["id"])

    for name in TARGET_METRIC_NAMES:
        metric = metric_by_name.get(name)
        if not metric:
            continue
        for v in list_views_on_block(metric["id"], "Metric"):
            if v.get("friendlyName") in TARGET_VIEW_NAMES or v.get("friendlyName", "").startswith("TI "):
                delete_view(v["id"])
                deleted_views.append(v["id"])

    # Delete metrics
    deleted_metrics = []
    for name in TARGET_METRIC_NAMES:
        metric = metric_by_name.get(name)
        if metric:
            delete_metric(metric["id"])
            deleted_metrics.append(metric["id"])

    # Delete lists
    deleted_lists = []
    for name in TARGET_LIST_NAMES:
        lst = list_by_name.get(name)
        if lst:
            delete_list(lst["id"])
            deleted_lists.append(lst["id"])

    print(json.dumps({
        "deleted_boards": deleted_boards,
        "deleted_views": deleted_views,
        "deleted_metrics": deleted_metrics,
        "deleted_lists": deleted_lists
    }, indent=2))


if __name__ == "__main__":
    main()
