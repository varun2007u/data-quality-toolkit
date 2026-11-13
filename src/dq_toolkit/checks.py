"""Validation rules for a simple order dataset."""

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    failed_rows: int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


REQUIRED_COLUMNS = {"order_id", "customer_id", "order_date", "status", "amount"}
VALID_STATUSES = {"pending", "completed", "cancelled", "refunded"}


def profile_orders(frame: pd.DataFrame) -> list[Finding]:
    """Return validation findings for an orders DataFrame."""
    missing = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    findings: list[Finding] = []
    if missing:
        findings.append(Finding(
            rule="required_columns",
            severity="error",
            failed_rows=len(missing),
            message=f"Missing required columns: {', '.join(missing)}",
        ))

    if "order_id" in frame:
        findings.append(Finding(
            "order_id_not_null", "error", int(frame["order_id"].isna().sum()),
            "Order identifiers must be populated.",
        ))
        duplicate_mask = frame["order_id"].notna() & frame["order_id"].duplicated(keep=False)
        findings.append(Finding(
            "order_id_unique", "error", int(duplicate_mask.sum()),
            "An order identifier should occur once.",
        ))

    for column in ("customer_id", "order_date", "status"):
        if column in frame:
            findings.append(Finding(
                f"{column}_not_null", "error", int(frame[column].isna().sum()),
                f"{column} must be populated.",
            ))

    if "status" in frame:
        invalid = frame["status"].notna() & ~frame["status"].isin(VALID_STATUSES)
        findings.append(Finding(
            "status_in_domain", "error", int(invalid.sum()),
            "Status must be pending, completed, cancelled, or refunded.",
        ))

    if "amount" in frame:
        numeric = pd.to_numeric(frame["amount"], errors="coerce")
        invalid = numeric.isna() | (numeric < 0)
        findings.append(Finding(
            "amount_non_negative_numeric", "error", int(invalid.sum()),
            "Amount must be numeric and greater than or equal to zero.",
        ))

    if "order_date" in frame:
        parsed = pd.to_datetime(frame["order_date"], errors="coerce")
        invalid = frame["order_date"].notna() & parsed.isna()
        findings.append(Finding(
            "order_date_parseable", "error", int(invalid.sum()),
            "Order date must be parseable as a date.",
        ))

    return findings
