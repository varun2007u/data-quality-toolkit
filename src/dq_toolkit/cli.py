"""Command-line entry point."""

import argparse
import json
from pathlib import Path

import pandas as pd

from .checks import profile_orders


def main() -> int:
    parser = argparse.ArgumentParser(description="Run data-quality checks on an orders CSV.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    profile = subparsers.add_parser("profile", help="Profile and validate an orders CSV.")
    profile.add_argument("csv_path", type=Path)
    profile.add_argument("--output", type=Path, help="Optional path for a JSON report.")
    args = parser.parse_args()

    frame = pd.read_csv(args.csv_path)
    findings = profile_orders(frame)
    report = {
        "file": str(args.csv_path),
        "rows_checked": int(len(frame)),
        "findings": [finding.to_dict() for finding in findings],
        "error_count": sum(f.failed_rows > 0 and f.severity == "error" for f in findings),
    }
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
