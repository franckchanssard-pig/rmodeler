# Lists, Dimensions, and Blocks

Goal: structure models correctly from the start.

## 1) Understand list types
- **Dimension lists** define the structure of metrics (and drive aggregation).
- **Transaction lists** store granular events and are often aggregated into metrics.

## 2) Dimensional consistency
- A metric’s dimensions should match its intended use.
- Avoid mixing unrelated dimensions; prefer helper metrics to reshape outputs.

## 3) Use list properties intentionally
- Default property is used for display and common references.
- Keep technical names stable; rename with caution.

## 4) When to use a transaction list
- When you need row‑level data and will aggregate using BY or SELECT.
- Avoid using transaction lists directly as metric dimensions unless necessary.

## 5) Modeling hygiene
- Remove unused lists and properties.
- Document list purpose and ownership.

## Sources (Pigment KB)
```
https://kb.pigment.com/docs/model-lists
https://kb.pigment.com/docs/understand-dimension-transaction-lists
https://kb.pigment.com/docs/understand-pigment-blocks
```
