import warnings

import pandas as pd

from dq_toolkit.checks import profile_orders


def clean_orders():
    return pd.DataFrame({
        "order_id": ["O-100", "O-101"],
        "customer_id": ["C-1", "C-2"],
        "order_date": ["2026-01-03", "2026-01-04"],
        "status": ["completed", "pending"],
        "amount": [120.50, 75.00],
    })


def test_clean_data_has_no_failed_rules():
    findings = profile_orders(clean_orders())
    assert all(item.failed_rows == 0 for item in findings)


def test_duplicate_order_id_is_detected():
    frame = clean_orders()
    frame.loc[1, "order_id"] = "O-100"
    findings = {item.rule: item for item in profile_orders(frame)}
    assert findings["order_id_unique"].failed_rows == 2


def test_invalid_status_and_negative_amount_are_detected():
    frame = clean_orders()
    frame.loc[0, "status"] = "in_transit"
    frame.loc[1, "amount"] = -10
    findings = {item.rule: item for item in profile_orders(frame)}
    assert findings["status_in_domain"].failed_rows == 1
    assert findings["amount_non_negative_numeric"].failed_rows == 1


def test_missing_required_columns_are_reported_without_crashing():
    frame = clean_orders().drop(columns=["customer_id", "amount"])
    findings = {item.rule: item for item in profile_orders(frame)}
    assert findings["required_columns"].failed_rows == 2


def test_null_required_values_are_detected():
    frame = clean_orders()
    frame.loc[0, "order_id"] = None
    frame.loc[1, "customer_id"] = None
    findings = {item.rule: item for item in profile_orders(frame)}
    assert findings["order_id_not_null"].failed_rows == 1
    assert findings["customer_id_not_null"].failed_rows == 1


def test_unparseable_order_date_and_non_numeric_amount_are_detected():
    frame = clean_orders()
    frame.loc[0, "order_date"] = "2026-13-40"
    frame["amount"] = frame["amount"].astype("object")
    frame.loc[1, "amount"] = "not-a-number"
    # pandas may warn when inferring a format from intentionally invalid input.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Could not infer format.*",
            category=UserWarning,
        )
        findings = {item.rule: item for item in profile_orders(frame)}
    assert findings["order_date_parseable"].failed_rows == 1
    assert findings["amount_non_negative_numeric"].failed_rows == 1
