"""
------------------------------------------------------------------------------
Reconciler Core Module for Mini Reconciliation Tool

This module defines the main Reconciler class, which orchestrates the full
reconciliation workflow from raw input DataFrames to final classified outputs.

Responsibilities:
  - Loads configuration using ConfigLoader.
  - Merges internal and provider DataFrames on a transaction key.
  - Classifies merged rows into categories: matched, only in internal,
    only in provider, mismatched.
  - Finalizes results by cleaning and renaming columns for output.

Key Component:
- Reconciler: Central class that encapsulates and coordinates all core steps
  for reconciling two transaction files in a reusable, testable way.

This design makes the reconciliation logic modular, traceable, and easy to extend.
------------------------------------------------------------------------------
"""

from typing import Dict
from pandas import DataFrame
from src import logger
from src.mini_reconcile.config.configurations import ConfigLoader
from src.mini_reconcile.core.reader import load_csv
from src.mini_reconcile.core.merger import merge_dataframes
from src.mini_reconcile.core.classifier import classify_merged_rows
from src.mini_reconcile.core.finalizer import finalize_results


class Reconciler:
    def __init__(self, config_path: str = None) -> None:
        logger.info("Initializing Reconciler...")
        self.config = ConfigLoader(config_path).load()

    def reconcile(self, df_internal, df_provider):
        merged = merge_dataframes(df_internal, df_provider, self.config)
        results = classify_merged_rows(merged, self.config)
        final = finalize_results(results, self.config)

        logger.info("Reconciliation complete.")
        return final