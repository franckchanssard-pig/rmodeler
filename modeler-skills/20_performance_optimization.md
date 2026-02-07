# Performance and Optimization

Goal: keep models fast and stable as they scale.

## 1) Use Performance Insights regularly
- Identify the **most time‑consuming metrics** and dense blocks.
- Focus on a small set of slow objects rather than broad refactors.
- Remove unused blocks or views that add compute cost.

## 2) Scope calculations early and keep them scoped
- Apply scoped calculations as early as possible.
- Maintain the same scoping dimensions across downstream metrics to avoid scope loss.
- If scope is lost, the calculation will recompute for the full space.

## 3) Profile calculation paths
- Use profiling after **real updates** to see the actual calculation path.
- Identify which blocks/metrics are responsible for slowdowns.
- Keep a log of high‑cost formulas and refactor them.

## 4) Refactoring patterns
- Split complex formulas into helper metrics and reuse them.
- Avoid repeated large FILTER/SELECT operations; compute once and reuse.
- Minimize dense outputs when a sparse metric is sufficient.

## 5) Performance review checklist
- Top slow metrics identified in Performance Insights
- Scoped calculations applied early
- Calculation paths profiled after updates
- Dense blocks reduced or removed
- Helper metrics reused rather than recomputed

## Sources (Pigment KB)
```
https://kb.pigment.com/docs/model-performance
https://kb.pigment.com/docs/use-performance-insights
https://kb.pigment.com/docs/optimize-formulas-scoped-calculations
https://kb.pigment.com/docs/profile-calculation-paths
```
