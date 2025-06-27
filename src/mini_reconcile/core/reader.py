"""
------------------------------------------------------------------------------
CSV Reader Module for Mini Reconciliation Tool

This module handles loading input CSV files into DataFrames with logging
and robust error handling. It supports:
  - Reading any CSV file given its file path.
  - Logging row counts and parse status.
  - Graceful handling of missing or malformed files with clear error messages.

Key Function:
- load_csv: Loads a CSV file and returns it as a pandas DataFrame,
  logging progress and raising descriptive errors on failure.

This ensures the tool can reliably process user-uploaded transaction files.
------------------------------------------------------------------------------
"""

import pandas as pd
from pandas import DataFrame
from src import logger


def load_csv(path: str, label: str) -> DataFrame:
    logger.info(f"Reading {label} CSV: {path}")
    try:
        df = pd.read_csv(path)
        logger.info(f"{label} CSV loaded: {df.shape[0]} rows")
        return df
    except FileNotFoundError:
        logger.error(f"{label} CSV not found: {path}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"{label} CSV parse failed: {e}")
        raise ValueError(f"{label} CSV parse failed: {path}") from e
    