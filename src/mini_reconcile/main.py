"""
------------------------------------------------------------------------------
Command-Line Entry Point for Mini Reconciliation Tool

This script provides a simple CLI interface for running the full reconciliation
process end-to-end.

Responsibilities:
  - Parses user arguments for input CSV file paths.
  - Loads the input files as DataFrames.
  - Invokes the Reconciler to merge, classify, and finalize results.
  - Prints a summary of each reconciliation category to the console.

Usage:
  python main.py <internal_csv> <provider_csv>

This makes it easy to test and validate the reconciliation logic outside the UI.
------------------------------------------------------------------------------
"""

import argparse
from src.mini_reconcile.core.reconciler import Reconciler
from src.mini_reconcile.core.reader import load_csv


def main():
    parser = argparse.ArgumentParser(description="Run reconciliation.")
    parser.add_argument("internal_csv", help="Path to internal CSV")
    parser.add_argument("provider_csv", help="Path to provider CSV")
    args = parser.parse_args()

    reconciler = Reconciler()

    # ✅ ADD THIS:
    df_internal = load_csv(args.internal_csv, "Internal System Export")
    df_provider = load_csv(args.provider_csv, "Provider Statement")

    results = reconciler.reconcile(df_internal, df_provider)

    for label, df in results.items():
        print(f"\n=== {label.upper()} ===")
        print(df.head())



if __name__ == "__main__":
    main()
