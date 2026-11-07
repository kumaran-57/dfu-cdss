# Standardized Experiment Results Template

Use this template to document real experimental evaluations. Never fabricate numbers.

---

## Run Metadata
- **Experiment ID**: (e.g. E1, E2, E7)
- **Execution Date**: YYYY-MM-DD
- **Hardware Used**: CPU / GPU identifier, RAM, driver version
- **Random Seed**: 42
- **Manifest Hash**: SHA256 of data split manifest
- **Dataset Source**: (e.g., DFUC2020 / Synthetic Benchmark)

---

## Quantitative Outcomes

| Model / Configuration | Split | Metric 1 (Mean ± 95% CI) | Metric 2 (Mean ± 95% CI) | Latency (ms) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Baseline | Test | ... | ... | ... | ... |
| Candidate Method | Test | ... | ... | ... | ... |

---

## Subgroup & Error Analysis
- Performance stratified by camera device / image quality tier.
- Identified failure modes (e.g. macerated boundary, heavy shadowing).
