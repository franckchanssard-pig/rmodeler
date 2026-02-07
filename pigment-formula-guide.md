# Pigment formula guide ("perfect formula" checklist)

This guide focuses on **syntax + structure** so your formulas are correct, readable, and easy to maintain.

## 0) Prerequisites
- You need **Configure Blocks** permission to write formulas.

## 1) Basic building blocks
- **Metrics and list properties** are your primary references.
- **List items** use double quotes.

Examples (syntax patterns):
- `Country."France"`
- `Employee."Ben"`
- `Revenue[Month."Jan 21"]`

Tip: You can omit the property if you want the **default property**.

## 2) Modifiers overview (most-used syntax)

### FILTER
Keep only items/values that match a boolean expression.
```
expression[FILTER: filtering_expression]
```

### EXCLUDE
Exclude items/values (opposite of FILTER). Use `CurrentValue` to avoid repeating long expressions.
```
expression[EXCLUDE: filtering_expression]
```

### SELECT
Filter + aggregate in one step (equivalent to FILTER then REMOVE on dimensions).
```
source_metric[SELECT AGGREGATOR: boolean_expression]
```

### REMOVE
Remove dimensions from a block (aggregate over them).
```
source_block[REMOVE [aggregator]: dimension1[, dimension2]]
```

### KEEP
Keep only specific dimensions and aggregate the rest.
```
source_block[KEEP [aggregator] [ON RANK(<dimension1>)]: dimension2[, dimension3]]
```
Note: `ON RANK` is required when KEEP retains multiple dimensions with `FIRST` or `FIRSTNONBLANK`.

### ADD
Add dimensions and allocate values across them.
```
input_block[ADD AllocationMethod: dimension1, dimension2]
```
Allocation methods include `CONSTANT` (default) and `SPLIT`.

### BY
Transform data between lists/dimensions using mapping attributes. Handles aggregation or allocation depending on relationship.
```
source_block[BY aggregation_method: mapping_attribute]
source_block[BY allocation_method: mapping_attribute]
```

## 3) Aggregation methods (common)
When you see an optional `aggregator` in REMOVE/KEEP/SELECT/BY, typical ones include:
- `SUM` (default for number)
- `AVG`
- `MEDIAN`
- `MIN`, `MAX`
- `FIRST`, `FIRSTNONBLANK`
- `STDEVS`, `STDEVP`

## 4) Readability and "perfect" formatting
- Use line breaks and indentation to show structure.
- Use comments for explanation:
  - `// inline comment`
  - `/* block comment */`
- Use Prettify (in the formula editor) to auto-format.

## 5) Quick patterns to memorize
- **Filter by item:**
  - `Revenue[SELECT: Country = Country."FR"]`
- **Filter by value:**
  - `Revenue[FILTER: Revenue > 1000]`
- **Exclude values using CurrentValue:**
  - `Revenue[EXCLUDE: CurrentValue > 1000]`
- **Aggregate by removing dimensions:**
  - `Revenue[REMOVE SUM: Country]`
- **Keep only one dimension:**
  - `Revenue[KEEP SUM: Month]`
- **Add a dimension with allocation:**
  - `Revenue[ADD SPLIT: Product]`
- **Roll up using mapping:**
  - `Revenue[BY SUM: Country.Region]`

## 6) Validation + troubleshooting habits
- Use the **Formula Playground (Auto mode)** to confirm return data type and dimensionality.
- If a formula is long, test it in sections (comment parts out).
- Avoid circular references unless using dedicated iterative functions.

---

# Sources (Pigment KB)
- Introduction to Formulas
- FILTER / EXCLUDE / SELECT / ADD / REMOVE / KEEP / BY modifier docs
- How to make formulas easier to understand
- Troubleshoot your formulas
