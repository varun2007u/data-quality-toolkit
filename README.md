# Data Quality Toolkit

A small, reproducible Python + SQL project for checking the reliability of analytical datasets before they reach dashboards or downstream consumers.

## What it demonstrates
- Dataset profiling and explicit validation rules
- Key, completeness, domain, and numeric-range checks
- A command-line report that can be used in a lightweight pipeline
- Equivalent SQL checks for warehouse-side validation
- Unit tests and a deliberately imperfect synthetic dataset

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -e ".[dev]"
pytest
dq-check profile data/orders.csv
```

The CLI exits with status 1 when validation errors are found, making it suitable for a CI or scheduled-job gate.

## Project layout

- `src/dq_toolkit/checks.py` — reusable validation rules
- `src/dq_toolkit/cli.py` — command-line interface and JSON output
- `tests/` — tests for clean and defective input
- `data/orders.csv` — synthetic example data with known defects
- `sql/orders_quality_checks.sql` — warehouse-side equivalents

## Rules included
1. Required columns are present.
2. `order_id` is unique and non-null.
3. `customer_id`, `order_date`, and `status` are populated.
4. Status is one of `pending`, `completed`, `cancelled`, or `refunded`.
5. `amount` is numeric and non-negative.
6. `order_date` can be parsed as a date.

## Example

```bash
dq-check profile data/orders.csv --output report.json
```

The sample file is synthetic and intentionally contains a few data-quality issues. It is not sourced from a real customer or financial institution.

## Design notes
This is an illustrative starter, not a production data-quality platform. Production use would add configurable rules, severity thresholds, partition-aware checks, structured logging, orchestration integration, and trend storage. See [the SQL checks](sql/orders_quality_checks.sql) for a second implementation of the same control ideas.
