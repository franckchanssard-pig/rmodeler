# Formula Syntax and Modifiers

Focus: writing correct, readable, and maintainable Pigment formulas.

## 1) Formula composition rules
- A formula is evaluated in a **dimensional context**; modifiers change that context.
- Prefer **short, composable formulas** over long nested expressions.
- Use the **Formula Playground** and **Auto format** to validate structure and output shape.

## 2) Core modifiers and when to use them

### FILTER
Use to keep only items that match a boolean condition.
```
expr[FILTER: condition]
```
- Good for removing rows before aggregation.

### EXCLUDE
Use to remove items matching a condition (opposite of FILTER).
```
expr[EXCLUDE: condition]
```
- Use `CurrentValue` to avoid repeating expressions.

### SELECT
Filter + aggregate in one step (FILTER + REMOVE in one operation).
```
metric[SELECT AGGREGATOR: condition]
```
- Great for point‑in‑time or conditional aggregation.

### REMOVE
Aggregate over specified dimensions (drop them).
```
block[REMOVE [AGGREGATOR]: dim1, dim2]
```
- Use when you need totals independent of a dimension.

### KEEP
Keep only certain dimensions and aggregate over all others.
```
block[KEEP [AGGREGATOR] [ON RANK(dim)]: dim2, dim3]
```
- Use when you need a block at a specific granularity.

### ADD
Add a dimension and distribute values across it.
```
block[ADD AllocationMethod: dim]
```
- Common allocation methods: `CONSTANT`, `SPLIT`.

### BY
Transform data using a mapping attribute (can aggregate or allocate depending on relationship).
```
block[BY AGGREGATOR: mapping_attribute]
block[BY AllocationMethod: mapping_attribute]
```
- Use for roll‑ups and hierarchical mappings.

## 3) Combining modifiers (order matters)
- When multiple modifiers are chained, **evaluate left to right** and reason about the resulting dimensionality.
- Prefer **FILTER/SELECT early**, then REMOVE/KEEP/ADD to shape output.

## 4) Common patterns
- Conditional aggregation:
  - `Sales[SELECT SUM: Country = Country."FR"]`
- Remove dimension for totals:
  - `Sales[REMOVE SUM: Country]`
- Keep a single dimension:
  - `Sales[KEEP SUM: Month]`
- Allocation across dimension:
  - `Budget[ADD SPLIT: Department]`
- Roll‑up using mapping:
  - `Sales[BY SUM: Product.Category]`

## 5) Quality checklist ("perfect formula")
- Uses correct modifiers for intent (FILTER vs SELECT vs REMOVE).
- Output dimensions match the expected target block.
- Readability: formatted, minimal nested logic, comments added when non‑obvious.
- No redundant recalculation (reuse helper metrics if needed).
- Tested in Playground and validated on sample data.

## Sources (Pigment KB)
```
https://kb.pigment.com/docs/introduction-formulas
https://kb.pigment.com/docs/filter-modifier
https://kb.pigment.com/docs/exclude-modifier
https://kb.pigment.com/docs/select-modifier
https://kb.pigment.com/docs/remove-modifier
https://kb.pigment.com/docs/keep-modifier
https://kb.pigment.com/docs/add-modifier
https://kb.pigment.com/docs/by-modifier
https://kb.pigment.com/docs/modifiers-in-modeling
https://kb.pigment.com/docs/formula-wizard-by-modifier
https://kb.pigment.com/docs/filter-data-in-formulas
https://kb.pigment.com/docs/by-mapping-parameter-arrow
```
