# Pigment formula fetch (metrics)

This quick flow resolves a metric's formula using the workspace API.

## Prereqs
- VPN connected
- Bearer token in `TOKEN`
- Org/app IDs

```bash
export TOKEN='<BEARER_TOKEN>'
export ORG_ID='5371eb8c-30e7-48cc-91b2-4d1c4a389d79'
export APP_ID='0538f210-83af-4474-9b03-812a0c15e1ce'
```

## 1) Get the formula for a metric
Use the metric ID as `searchId`:

```bash
METRIC_ID='03bac038-1fa1-4d0d-8dc9-5a87365cfaee'

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  "https://staging.pigment.app/api/workspace/internals/formula/FindFormulasBySearchId?organizationId=$ORG_ID&searchId=$METRIC_ID"
```

This returns an array of `FormulaAudit` with `rawFormula`.

## 2) (Optional) Resolve formula group IDs for a metric
If you need groups (e.g., for history):

```bash
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  "https://staging.pigment.app/api/workspace/$APP_ID/metric/GetFormulaGroups/$METRIC_ID"
```

## 3) (Optional) Formula history for a metric formula group
Take the `formulaGroupId` from step 2 and call:

```bash
FORMULA_GROUP_ID='3df05684-ee43-4e5d-8bed-e068723da68c'

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"metricFormulaGroup":{"metricId":"'"$METRIC_ID"'","formulaGroupId":"'"$FORMULA_GROUP_ID"'"}}' \
  "https://staging.pigment.app/api/workspace/internals/formula/ListFormulaHistoryForTarget/$APP_ID"
```

## Notes
- `/api/v1/blocks` does not accept this bearer token (401); use `/api/workspace/...`.
- `FindFormulasBySearchId` works for metric IDs and returns raw formulas.
