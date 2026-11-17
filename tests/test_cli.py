import json

import pandas as pd

from dq_toolkit.cli import main


def test_cli_writes_json_report_and_returns_failure_for_invalid_data(tmp_path, monkeypatch, capsys):
    source = tmp_path / "orders.csv"
    output = tmp_path / "report.json"
    pd.DataFrame({
        "order_id": ["O-1"],
        "customer_id": ["C-1"],
        "order_date": ["2026-01-01"],
        "status": ["unknown"],
        "amount": [10],
    }).to_csv(source, index=False)
    monkeypatch.setattr(
        "sys.argv",
        ["dq-check", "profile", str(source), "--output", str(output)],
    )

    assert main() == 1
    file_report = json.loads(output.read_text(encoding="utf-8"))
    console_report = json.loads(capsys.readouterr().out)
    assert file_report["rows_checked"] == 1
    assert file_report["error_count"] == 1
    assert console_report == file_report


def test_cli_returns_success_for_clean_data(tmp_path, monkeypatch, capsys):
    source = tmp_path / "orders.csv"
    pd.DataFrame({
        "order_id": ["O-1"],
        "customer_id": ["C-1"],
        "order_date": ["2026-01-01"],
        "status": ["completed"],
        "amount": [10],
    }).to_csv(source, index=False)
    monkeypatch.setattr("sys.argv", ["dq-check", "profile", str(source)])

    assert main() == 0
    assert json.loads(capsys.readouterr().out)["error_count"] == 0
