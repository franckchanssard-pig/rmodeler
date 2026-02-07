#!/usr/bin/env python3
import os, json, urllib.request
from urllib.parse import quote
from urllib.error import HTTPError

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise SystemExit("Set TOKEN env var to your Bearer token")

APP_ID = os.environ.get("APP_ID", "0538f210-83af-4474-9b03-812a0c15e1ce")
ORG_ID = os.environ.get("ORG_ID", "5371eb8c-30e7-48cc-91b2-4d1c4a389d79")
API_HOST = os.environ.get("API_HOST", "https://staging.pigment.app")
BASE_APP = f"{API_HOST}/api/workspace/{APP_ID}"
BASE_WS = f"{API_HOST}/api/workspace"

BASE_DIM = os.environ.get("BASE_DIM", "b6a69813-d214-4980-a2ec-7ffb348fbd43")  # Field 1
BASE_TX = os.environ.get("BASE_TX", "7f999943-b1d1-43b7-b5c4-7134323595a6")   # test rmodeler

# Seed data (examples)
SEED_EMPLOYEES = [
    "Fran", "Rober", "Aurel", "Max", "Jeff", "Ahmed",
    "Jeremy", "Thomas", "Mathieu", "Franck"
]
SEED_ACCOUNTS = [
    "Internal", "Client A", "Client B"
]
SEED_PROJECTS = [
    ("Project Alpha", "Internal", "In Progress", True),
    ("Project Beta", "Client A", "Planned", True),
    ("Project Gamma", "Client B", "In Progress", True),
    ("Project Delta", "Internal", "On Hold", False),
    ("Project Epsilon", "Client A", "Complete", False),
    ("Project Zeta", "Client B", "Planned", True),
]


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


def list_all():
    return request("GET", "/list/ListForApplication")[1] or []


def get_list(list_id):
    return request("GET", f"/list/Get/{list_id}")[1]


def duplicate_list(list_id, new_name):
    # This environment expects the new name as a JSON string body.
    path = f"/list/DuplicateList?listToDuplicateId={list_id}"
    return request("POST", path, new_name)[1]


def create_list_with_default_view(name, is_dimension, properties):
    payload = {
        "friendlyName": name,
        "isDimension": is_dimension,
        "readableByEveryone": True,
        "properties": properties
    }
    try:
        return request("POST", "/list/CreateWithDefaultView", payload)[1]
    except SystemExit as e:
        # Some environments require a wrapped request object.
        if "request" in str(e).lower():
            return request("POST", "/list/CreateWithDefaultView", {"request": payload})[1]
        # Some environments require PascalCase field names.
        if "Properties" in str(e):
            payload_pc = {
                "FriendlyName": name,
                "IsDimension": is_dimension,
                "ReadableByEveryone": True,
                "Properties": properties
            }
            return request("POST", "/list/CreateWithDefaultView", payload_pc)[1]
        raise


def extract_created_id(resp):
    if not resp:
        return None
    if isinstance(resp, dict):
        if "id" in resp:
            return resp["id"]
        for key in ("list", "createdList", "result"):
            val = resp.get(key)
            if isinstance(val, dict) and "id" in val:
                return val["id"]
    return None


def get_list_display_data(list_id):
    # Try GET first; fallback to POST with empty payload.
    try:
        return request("GET", f"/list/GetDisplayData/{list_id}")[1]
    except SystemExit:
        return request("POST", f"/list/FindDisplayData/{list_id}", {})[1]


def extract_modality_ids(display_data):
    if not display_data:
        return []
    ids = []
    if isinstance(display_data, dict):
        # Common shapes: {"modalities": [{"id":...}, ...]} or {"rows": [...]}
        for key in ("modalities", "rows", "items", "listItems"):
            val = display_data.get(key)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        for id_key in ("id", "modalityId", "rowId"):
                            if id_key in item:
                                ids.append(item[id_key])
                                break
        # If the response is already a list-like dict with "values"
        vals = display_data.get("values")
        if isinstance(vals, list):
            for item in vals:
                if isinstance(item, dict) and "id" in item:
                    ids.append(item["id"])
    elif isinstance(display_data, list):
        for item in display_data:
            if isinstance(item, dict) and "id" in item:
                ids.append(item["id"])
    return [i for i in ids if i]


def delete_list_modalities(list_id, modality_ids):
    if not modality_ids:
        return
    payloads = [
        {"listId": list_id, "modalityIds": modality_ids},
        {"listId": list_id, "listModalityIds": modality_ids},
        {"modalityIds": modality_ids},
        {"listModalityIds": modality_ids},
        {"request": {"listId": list_id, "modalityIds": modality_ids}},
        {"request": {"listId": list_id, "listModalityIds": modality_ids}},
        {"request": {"modalityIds": modality_ids}},
        {"request": {"listModalityIds": modality_ids}},
        {"Request": {"ListId": list_id, "ModalityIds": modality_ids}},
    ]
    last_err = None
    for payload in payloads:
        try:
            request("DELETE", f"/list/DeleteSelectedListModalities", payload)
            return
        except SystemExit as e:
            last_err = e
            continue
    if last_err:
        raise last_err


def rename_list(list_id, new_name):
    try:
        request("PUT", f"/list/Rename/{list_id}", {"friendlyName": new_name})
    except SystemExit:
        request("PUT", f"/list/Rename/{list_id}", new_name)


def add_property(list_id, prop):
    request("POST", f"/list/{list_id}/property/Add", prop)

def remove_property(list_id, prop_technical):
    request("DELETE", f"/list/{list_id}/property/Remove?propertyTechnicalName={prop_technical}")


def update_default_property(list_id, prop_technical):
    request("PUT", f"/list/{list_id}/property/UpdateDefaultProperty", {"request": {"newDefaultPropertyTechnicalName": prop_technical}})


def update_display_property(list_id, prop_technical):
    request("PUT", f"/list/{list_id}/property/UpdateDisplayProperty", prop_technical)


def add_rows(list_id, rows):
    payload = {"inputsOnExistingRows": [], "newRows": rows, "validateInputRows": True}
    request("PUT", f"/list/SetInputtedValuesWithNewRows?listId={list_id}", payload)


def clear_list_items(list_id):
    try:
        display = get_list_display_data(list_id)
        modality_ids = extract_modality_ids(display)
        delete_list_modalities(list_id, modality_ids)
    except SystemExit:
        pass


def ensure_empty_list(name, list_id, base_id, is_dimension, properties):
    clear_list_items(list_id)
    try:
        remaining = extract_modality_ids(get_list_display_data(list_id))
    except SystemExit:
        remaining = []
    if remaining:
        # Hard reset: delete the list and recreate.
        try:
            request("DELETE", f"/list/Remove/{list_id}")
        except SystemExit:
            return list_id
        existing = list_all()
        return ensure_dup(existing, name, base_id, is_dimension, properties)
    return list_id


def reset_list_properties(list_id, keep_friendly_names):
    lst = get_list(list_id)
    for p in lst["properties"]:
        if p.get("isAutoGenerated"):
            continue
        if p.get("friendlyName") in keep_friendly_names:
            continue
        remove_property(list_id, p["technicalName"])


def list_views_on_block(block_id, block_type="List"):
    path = f"/internals/view/ListViewsOnBlock?organizationId={ORG_ID}&blockType={block_type}&blockId={block_id}"
    return request("GET", path, base="workspace")[1] or []


def create_view(underlying_id, underlying_type, name, description):
    payload = {
        "underlyingType": underlying_type,
        "underlyingId": underlying_id,
        "friendlyName": name,
        "description": description,
        "newView": {
            "underlyingType": underlying_type,
            "underlyingId": underlying_id,
            "friendlyName": name,
            "description": description
        }
    }
    return request("POST", "/view/CreateViewWithDefaultConfig", payload)[1]


def find_view_on_block(block_id, block_type, name):
    for v in list_views_on_block(block_id, block_type):
        if v.get("friendlyName") == name:
            return v
    return None


def create_metric(name, description, dimensions):
    payload = {
        "friendlyName": name,
        "description": description,
        "dimensions": dimensions,
        "type": "Number",
        "visibility": "Local",
        "readableByEveryone": True
    }
    return request("POST", "/metric/CreateFromConfiguration", payload)[1]


def list_metrics():
    return request("GET", "/metric/ListForApplication")[1] or []


def find_metric_by_name(name):
    for m in list_metrics():
        if m.get("friendlyName") == name:
            return m
    return None


def get_formula_group(metric_id):
    resp = request("GET", f"/metric/GetFormulaGroups/{metric_id}")[1]
    if not resp:
        return None
    return next(iter(resp.keys()))


def create_formula(metric_id, formula_group_id, formula_string):
    payload = {
        "formulaString": formula_string,
        "replaceUserInputs": True,
        "enableOverridesIfNeeded": True
    }
    request("POST", f"/formula/CreateOnMetric/{metric_id}/{formula_group_id}", payload)


def create_board(name, description, blocks):
    payload = {
        "name": name,
        "description": description,
        "icon": "Input",
        "iconColor": "Blue",
        "boardSharingStatus": "Private",
        "blocks": blocks
    }
    return request("POST", "/board/Create", payload)[1]


def list_boards():
    return request("GET", "/board/List")[1] or []


def find_board_by_name(name):
    for b in list_boards():
        if b.get("name") == name or b.get("friendlyName") == name:
            return b
    return None


def update_board_blocks(board_id, blocks):
    payload = {"blocks": blocks}
    return request("PUT", f"/board/UpdateBlocks/{board_id}", payload)[1]


def ensure_dup(existing, name, base_id, is_dimension, properties):
    by_name = {l["friendlyName"].lower(): l for l in existing}
    by_id = {l["id"]: l for l in existing}
    key = name.lower()
    if key in by_name:
        return by_name[key]["id"]
    if base_id in by_id:
        list_id = by_id[base_id]["id"]
        rename_list(list_id, name)
        return list_id

    # If the configured base list doesn't exist, fall back to any list of the same type.
    fallback_base = next((l for l in existing if l.get("isDimension") == is_dimension), None)
    if fallback_base:
        dup = duplicate_list(fallback_base["id"], name)
        return dup["id"]

    # Last resort: attempt creation (may fail in some environments).
    created = create_list_with_default_view(name, is_dimension, properties)
    created_id = extract_created_id(created)
    if not created_id:
        raise SystemExit(f"CreateWithDefaultView did not return list id: {created}")
    return created_id


def recreate_list(name, base_id, is_dimension, properties):
    existing = list_all()
    by_name = {l["friendlyName"].lower(): l for l in existing}
    key = name.lower()
    if key in by_name:
        try:
            request("DELETE", f"/list/Remove/{by_name[key]['id']}")
        except SystemExit:
            # If we can't delete, fall back to reusing existing.
            return by_name[key]["id"]
    existing = list_all()
    return ensure_dup(existing, name, base_id, is_dimension, properties)


def main():
    existing = list_all()
    dim_properties = [{
        "friendlyName": "Name Public",
        "type": "Text",
        "isUnique": False,
        "readableByEveryone": True,
        "isAutoGenerated": False
    }]
    time_properties = [{
        "friendlyName": "Date",
        "type": "Date",
        "isUnique": False,
        "readableByEveryone": True,
        "isAutoGenerated": False
    }]

    # Force clean lists (delete then recreate) so no duplicated items remain.
    employee_id = recreate_list("TI Employee", BASE_DIM, True, dim_properties)
    account_id = recreate_list("TI Account", BASE_DIM, True, dim_properties)
    project_id = recreate_list("TI Project", BASE_DIM, True, dim_properties)
    time_id = recreate_list("TI Time Entry", BASE_TX, False, time_properties)

    # Dimension lists: reset properties and items, then ensure Name property.
    for lid in [employee_id, account_id, project_id]:
        reset_list_properties(lid, {"Name Public", "Name"})
        lst = get_list(lid)
        props = {p["friendlyName"]: p for p in lst["properties"]}
        if "Name Public" not in props and "Name" not in props:
            add_property(lid, {"friendlyName": "Name Public", "type": "Text", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False})
            lst = get_list(lid)
            props = {p["friendlyName"]: p for p in lst["properties"]}
        pref = props.get("Name Public") or props.get("Name")
        update_default_property(lid, pref["technicalName"])
        update_display_property(lid, pref["technicalName"])
        clear_list_items(lid)

    # Project extra properties
    proj_list = get_list(project_id)
    proj_props = {p["friendlyName"] for p in proj_list["properties"]}
    if "Account" not in proj_props:
        add_property(project_id, {"friendlyName": "Account", "type": "Dimension", "referencedDimensionId": account_id, "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False})
    if "Status" not in proj_props:
        add_property(project_id, {"friendlyName": "Status", "type": "Text", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False})
    if "Active" not in proj_props:
        add_property(project_id, {"friendlyName": "Active", "type": "Boolean", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False})

    # Time Entry list: reset properties/items, then ensure required properties exist
    reset_list_properties(time_id, {"Date", "Employee", "Project", "Account", "Hours", "Note", "Status", "Last Updated By", "Last Updated At"})
    te_list = get_list(time_id)
    props = {p["friendlyName"] for p in te_list["properties"]}
    required = [
        ("Date", {"friendlyName": "Date", "type": "Date", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Employee", {"friendlyName": "Employee", "type": "Dimension", "referencedDimensionId": employee_id, "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Project", {"friendlyName": "Project", "type": "Dimension", "referencedDimensionId": project_id, "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Account", {"friendlyName": "Account", "type": "Dimension", "referencedDimensionId": account_id, "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Hours", {"friendlyName": "Hours", "type": "Number", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Note", {"friendlyName": "Note", "type": "Text", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Status", {"friendlyName": "Status", "type": "Text", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Last Updated By", {"friendlyName": "Last Updated By", "type": "Text", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
        ("Last Updated At", {"friendlyName": "Last Updated At", "type": "Date", "isUnique": False, "readableByEveryone": True, "isAutoGenerated": False}),
    ]
    for name, spec in required:
        if name not in props:
            add_property(time_id, spec)

    te_list = get_list(time_id)
    prop_date = next(p for p in te_list["properties"] if p["friendlyName"] == "Date")["technicalName"]
    update_default_property(time_id, prop_date)
    update_display_property(time_id, prop_date)
    clear_list_items(time_id)

    # Seed Employee list
    emp_list = get_list(employee_id)
    emp_name_prop = next(p for p in emp_list["properties"] if p["friendlyName"] in ("Name Public", "Name"))["technicalName"]
    emp_rows = [{"inputs": [{"propertyTechnicalName": emp_name_prop, "newValue": n}]} for n in SEED_EMPLOYEES]
    add_rows(employee_id, emp_rows)

    # Seed Account list
    acct_list = get_list(account_id)
    acct_name_prop = next(p for p in acct_list["properties"] if p["friendlyName"] in ("Name Public", "Name"))["technicalName"]
    acct_rows = [{"inputs": [{"propertyTechnicalName": acct_name_prop, "newValue": n}]} for n in SEED_ACCOUNTS]
    add_rows(account_id, acct_rows)

    # Seed Project list
    proj_list = get_list(project_id)
    proj_props = {p["friendlyName"]: p["technicalName"] for p in proj_list["properties"]}
    proj_rows = []
    for name, account, status, active in SEED_PROJECTS:
        proj_rows.append({
            "inputs": [
                {"propertyTechnicalName": proj_props["Name Public"] if "Name Public" in proj_props else proj_props["Name"], "newValue": name},
                {"propertyTechnicalName": proj_props["Account"], "newValue": account},
                {"propertyTechnicalName": proj_props["Status"], "newValue": status},
                {"propertyTechnicalName": proj_props["Active"], "newValue": active},
            ]
        })
    add_rows(project_id, proj_rows)

    # Create or reuse views
    time_view = find_view_on_block(time_id, "List", "TI Time Entry")
    if not time_view:
        time_view = create_view(time_id, "List", "TI Time Entry", "Time entry input")

    project_view = find_view_on_block(project_id, "List", "TI Projects")
    if not project_view:
        project_view = create_view(project_id, "List", "TI Projects", "Projects and account mapping")

    # Create or reuse metric + formula
    metric = find_metric_by_name("TI Hours")
    if not metric:
        metric = create_metric("TI Hours", "Total hours by employee/project/account", [employee_id, project_id, account_id])
    metric_id = metric["metric"]["id"] if "metric" in metric else metric.get("id")
    fg = get_formula_group(metric_id)

    te_list = get_list(time_id)
    prop_map = {p["friendlyName"]: p for p in te_list["properties"]}
    hours = prop_map["Hours"]["technicalName"]
    emp = prop_map["Employee"]["technicalName"]
    proj = prop_map["Project"]["technicalName"]
    acct = prop_map["Account"]["technicalName"]

    formula = (
        f"$list({time_id}, \"'TI Time Entry'\").$property({time_id}, '{hours}', \"Hours\")"
        f"[by: $list({time_id}, \"'TI Time Entry'\").$property({time_id}, '{emp}', \"Employee\"), "
        f"$list({time_id}, \"'TI Time Entry'\").$property({time_id}, '{proj}', \"Project\"), "
        f"$list({time_id}, \"'TI Time Entry'\").$property({time_id}, '{acct}', \"Account\")]"
    )

    if fg:
        try:
            create_formula(metric_id, fg, formula)
        except SystemExit as e:
            if "already exists" not in str(e).lower():
                raise

    metric_view = find_view_on_block(metric_id, "Metric", "TI Hours")
    if not metric_view:
        metric_view = create_view(metric_id, "Metric", "TI Hours", "Hours totals")

    # Boards
    time_board_blocks = [
        {
            "blockId": time_view["id"],
            "blockType": "View",
            "boardBlockPosition": {"x": 0, "y": 0, "width": 8, "height": 10},
            "viewBoardBlockConfig": {
                "boardBlockDisplayType": "Table",
                "contentId": time_view["id"],
                "title": "Time Entry",
                "showTitle": True,
                "allowAddingNewItemsFromWidget": True
            }
        },
        {
            "blockId": project_view["id"],
            "blockType": "View",
            "boardBlockPosition": {"x": 8, "y": 0, "width": 4, "height": 10},
            "viewBoardBlockConfig": {
                "boardBlockDisplayType": "Table",
                "contentId": project_view["id"],
                "title": "Projects",
                "showTitle": True,
                "allowAddingNewItemsFromWidget": True
            }
        }
    ]

    time_board = find_board_by_name("Time Input")
    if time_board:
        try:
            update_board_blocks(time_board["id"], time_board_blocks)
        except SystemExit:
            pass
    else:
        time_board = create_board(
        "Time Input",
        "Timesheet entry and project maintenance",
        time_board_blocks
    )

    team_board_blocks = [
        {
            "blockId": metric_view["id"],
            "blockType": "View",
            "boardBlockPosition": {"x": 0, "y": 0, "width": 12, "height": 8},
            "viewBoardBlockConfig": {
                "boardBlockDisplayType": "Table",
                "contentId": metric_view["id"],
                "title": "Hours totals",
                "showTitle": True,
                "allowAddingNewItemsFromWidget": False
            }
        }
    ]

    team_board = find_board_by_name("Time Overview")
    if team_board:
        try:
            update_board_blocks(team_board["id"], team_board_blocks)
        except SystemExit:
            pass
    else:
        team_board = create_board(
        "Time Overview",
        "Manager overview and totals",
        team_board_blocks
    )

    print(json.dumps({
        "employee_list_id": employee_id,
        "account_list_id": account_id,
        "project_list_id": project_id,
        "time_entry_list_id": time_id,
        "time_entry_view_id": time_view["id"],
        "project_view_id": project_view["id"],
        "metric_id": metric_id,
        "metric_view_id": metric_view["id"],
        "time_input_board_id": time_board.get("id"),
        "time_overview_board_id": team_board.get("id")
    }, indent=2))


if __name__ == "__main__":
    main()
