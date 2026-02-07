#!/usr/bin/env python3
import os, json, urllib.request
from urllib.error import HTTPError

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise SystemExit('Set TOKEN env var to your Bearer token')

APP_ID = os.environ.get('APP_ID', '0538f210-83af-4474-9b03-812a0c15e1ce')
ORG_ID = os.environ.get('ORG_ID', '5371eb8c-30e7-48cc-91b2-4d1c4a389d79')
API_HOST = os.environ.get('API_HOST', 'https://staging.pigment.app')
BASE_APP = f"{API_HOST}/api/workspace/{APP_ID}"
BASE_WS = f"{API_HOST}/api/workspace"

# Existing list IDs (created earlier)
LIST_IDS = {
    "employee": "51d650cd-48f9-46e8-84c5-38513d0f112e",
    "account": "2368383b-4592-4c38-99b3-4e81d33a1cfc",
    "project": "8a8207b9-139d-4f08-9075-df733cf9a3f6",
    "time": "8dd95464-cbac-4220-90c0-91f6d105b005",
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


def get_list(list_id):
    return request("GET", f"/list/Get/{list_id}")[1]


def add_property(list_id, prop):
    request("POST", f"/list/{list_id}/property/Add", prop)


def update_default_property(list_id, prop_technical):
    request("PUT", f"/list/{list_id}/property/UpdateDefaultProperty", {"request": {"newDefaultPropertyTechnicalName": prop_technical}})


def update_display_property(list_id, prop_technical):
    # Endpoint expects a JSON string body.
    request("PUT", f"/list/{list_id}/property/UpdateDisplayProperty", prop_technical)


def add_rows(list_id, rows):
    payload = {"inputsOnExistingRows": [], "newRows": rows, "validateInputRows": True}
    request("PUT", f"/list/SetInputtedValuesWithNewRows?listId={list_id}", payload)


def create_view(underlying_id, underlying_type, name, description):
    # API seems to require both root fields and a nested newView object
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


def create_metric(name, description, dimensions):
    payload = {
        "friendlyName": name,
        "description": description,
        "dimensions": dimensions,
        "type": "Number",
        "visibility": "Local",
        "readableByEveryone": True
    }
    try:
        return request("POST", "/metric/CreateFromConfiguration", payload)[1]
    except SystemExit as e:
        # Idempotency: if a metric with the same name exists, reuse it.
        if "same name" in str(e) or "already a block with the same name" in str(e):
            existing = find_metric_by_name(name)
            if existing:
                return existing
        raise


def list_metrics():
    return request("GET", "/metric/ListForApplication")[1]


def find_metric_by_name(name):
    metrics = list_metrics() or []
    for m in metrics:
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
    try:
        return request("POST", "/board/Create", payload)[1]
    except SystemExit as e:
        # Idempotency: skip if the board already exists.
        if "same name already exists" in str(e):
            return None
        raise


def main():
    ids = dict(LIST_IDS)
    ids.update({
        "employee": os.environ.get("LIST_ID_EMPLOYEE", ids["employee"]),
        "account": os.environ.get("LIST_ID_ACCOUNT", ids["account"]),
        "project": os.environ.get("LIST_ID_PROJECT", ids["project"]),
        "time": os.environ.get("LIST_ID_TIME", ids["time"]),
    })
    ids_file = os.environ.get("TIME_INPUT_IDS_FILE")
    if ids_file and os.path.exists(ids_file):
        with open(ids_file, "r", encoding="utf-8") as f:
            ids.update(json.load(f))
    ids_json = os.environ.get("TIME_INPUT_IDS")
    if ids_json:
        ids.update(json.loads(ids_json))

    employee_id = ids["employee"]
    account_id = ids["account"]
    project_id = ids["project"]
    time_id = ids["time"]

    # Ensure Name Public exists on dimension lists and set default/display
    for lid in [employee_id, account_id, project_id]:
        lst = get_list(lid)
        props = {p["friendlyName"]: p for p in lst["properties"]}
        if "Name Public" not in props and "Name" not in props:
            add_property(lid, {"friendlyName":"Name Public","type":"Text","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
            lst = get_list(lid)
            props = {p["friendlyName"]: p for p in lst["properties"]}
        pref = props.get("Name Public") or props.get("Name")
        update_default_property(lid, pref["technicalName"])
        update_display_property(lid, pref["technicalName"])

    # Project extra properties
    proj_list = get_list(project_id)
    proj_props = {p["friendlyName"] for p in proj_list["properties"]}
    if "Account" not in proj_props:
        add_property(project_id, {"friendlyName":"Account","type":"Dimension","referencedDimensionId":account_id,"isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Status" not in proj_props:
        add_property(project_id, {"friendlyName":"Status","type":"Text","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Active" not in proj_props:
        add_property(project_id, {"friendlyName":"Active","type":"Boolean","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})

    # Time Entry properties (add missing only)
    te_list = get_list(time_id)
    te_props = {p["friendlyName"] for p in te_list["properties"]}
    if "Date" not in te_props:
        add_property(time_id, {"friendlyName":"Date","type":"Date","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Employee" not in te_props:
        add_property(time_id, {"friendlyName":"Employee","type":"Dimension","referencedDimensionId":employee_id,"isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Project" not in te_props:
        add_property(time_id, {"friendlyName":"Project","type":"Dimension","referencedDimensionId":project_id,"isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Account" not in te_props:
        add_property(time_id, {"friendlyName":"Account","type":"Dimension","referencedDimensionId":account_id,"isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Hours" not in te_props:
        add_property(time_id, {"friendlyName":"Hours","type":"Number","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Note" not in te_props:
        add_property(time_id, {"friendlyName":"Note","type":"Text","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Status" not in te_props:
        add_property(time_id, {"friendlyName":"Status","type":"Text","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Last Updated By" not in te_props:
        add_property(time_id, {"friendlyName":"Last Updated By","type":"Text","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})
    if "Last Updated At" not in te_props:
        add_property(time_id, {"friendlyName":"Last Updated At","type":"Date","isUnique":False,"readableByEveryone":True,"isAutoGenerated":False})

    te_list = get_list(time_id)
    date_prop = next(p for p in te_list["properties"] if p["friendlyName"] == "Date")
    update_default_property(time_id, date_prop["technicalName"])
    update_display_property(time_id, date_prop["technicalName"])

    # Seed Employee list + Internal account
    emp_list = get_list(employee_id)
    emp_name_prop = next(p for p in emp_list["properties"] if p["friendlyName"] in ("Name Public","Name"))["technicalName"]
    employees = ["Fran", "Rober", "Aurel", "Max", "Jeff", "Ahmed", "Jeremy", "Thomas", "Mathieu", "Franck"]
    emp_rows = [{"inputs":[{"propertyTechnicalName": emp_name_prop, "newValue": n}]} for n in employees]
    add_rows(employee_id, emp_rows)

    acct_list = get_list(account_id)
    acct_name_prop = next(p for p in acct_list["properties"] if p["friendlyName"] in ("Name Public","Name"))["technicalName"]
    add_rows(account_id, [{"inputs":[{"propertyTechnicalName": acct_name_prop, "newValue": "Internal"}]}])

    # Create views
    time_view = create_view(time_id, "List", "TI Time Entry", "Time entry input")
    project_view = create_view(project_id, "List", "TI Projects", "Projects and account mapping")

    # Create metric + formula
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
        create_formula(metric_id, fg, formula)

    metric_view = create_view(metric_id, "Metric", "TI Hours", "Hours totals")

    # Boards
    time_board = create_board(
        "Time Input",
        "Timesheet entry and project maintenance",
        [
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
    )

    team_board = create_board(
        "Time Overview",
        "Manager overview and totals",
        [
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
        "time_input_board_id": time_board.get("id") if time_board else None,
        "time_overview_board_id": team_board.get("id") if team_board else None
    }, indent=2))

if __name__ == '__main__':
    main()
