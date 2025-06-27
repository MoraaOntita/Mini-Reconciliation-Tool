"""
------------------------------------------------------------------------------
Data Merger Module for Mini Reconciliation Tool

This module provides the core function to merge the internal and provider
DataFrames based on a configurable merge key. It performs an outer join to
ensure that all transactions from both sources are accounted for, adds
configured suffixes to distinguish overlapping columns, and includes a
merge indicator to classify row origins.

Key Function:
- merge_dataframes: Merges two input DataFrames according to the YAML config,
  logs the process, and handles missing merge keys gracefully.

This is a critical step for detecting matched, missing, or mismatched transactions.
------------------------------------------------------------------------------
"""


from pandas import DataFrame
from src import logger


def merge_dataframes(df_internal: DataFrame, df_provider: DataFrame, config: dict) -> DataFrame:
    """
    Finalize the classified DataFrames by dropping internal columns,
    renaming columns for clarity, and retaining only relevant fields.

    :param results: Dictionary of classified DataFrames.
    :param config: Loaded configuration dictionary.
    :return: Dictionary of cleaned, renamed DataFrames ready for reporting or export.
    """

    logger.info("Merging DataFrames...")
    try:
        merged = df_internal.merge(
            df_provider,
            on=config['merge_key'],
            how='outer',
            suffixes=tuple(config['merge_suffixes']),
            indicator=config['merge_indicator']
        )
        logger.info(f"Merged DataFrame: {merged.shape}")
        return merged
    except KeyError as e:
        logger.error(f"Merge failed, key not found: {e}")
        raise
