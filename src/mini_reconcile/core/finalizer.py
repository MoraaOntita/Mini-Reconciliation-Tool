"""
------------------------------------------------------------------------------
Result Finalizer Module for Mini Reconciliation Tool

This module prepares the classified reconciliation results for presentation
or export. It performs final cleanup steps:
  - Drops the internal merge indicator column.
  - Renames columns for clearer output using configured mappings.
  - Ensures the result category column is included.

The final output is a dictionary of polished DataFrames, each corresponding
to a reconciliation category such as matched, only internal, only provider,
and mismatched.
------------------------------------------------------------------------------
"""


from typing import Dict
from pandas import DataFrame
from src import logger


def finalize_results(results: Dict[str, DataFrame], config: dict) -> Dict[str, DataFrame]:
    """
    Finalize the classified DataFrames by dropping internal columns,
    renaming columns for clarity, and retaining only relevant fields.

    :param results: Dictionary of classified DataFrames.
    :param config: Loaded configuration dictionary.
    :return: Dictionary of cleaned, renamed DataFrames ready for reporting or export.
    """
    
    logger.info("Finalizing classified results...")
    merge_col = config['merge_indicator']
    rename_cols = config['rename_columns']

    final = {}
    for key, df in results.items():
        cols = [col for col in df.columns if col != merge_col]
        if 'result' not in cols:
            cols.append('result')
        df = df[cols]
        df.rename(columns=rename_cols, inplace=True)
        final[key] = df
        logger.info(f"Finalized {key}: {df.shape[0]} rows")

    return final
