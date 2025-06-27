"""
------------------------------------------------------------------------------
Row Classifier Module for Mini Reconciliation Tool

This module defines logic for classifying merged transaction rows into
meaningful reconciliation categories based on the merge indicator and field
comparison rules from the configuration.

Categories:
  - Matched: Present in both files with identical values for all comparison fields.
  - Only Internal: Present only in the internal system export.
  - Only Provider: Present only in the provider statement.
  - Mismatched: Present in both but with differences in one or more key fields.

This separation enables clear reporting of matched records, missing records,
and discrepancies in amounts or statuses.
------------------------------------------------------------------------------
"""


from typing import Dict
from pandas import DataFrame
from src import logger


def classify_merged_rows(merged: DataFrame, config: dict) -> Dict[str, DataFrame]:
    """
    Classify merged transactions into matched, only_internal, only_provider,
    and mismatched groups.

    :param merged: DataFrame produced by merging internal and provider data.
    :param config: Loaded configuration dictionary.
    :return: Dictionary of DataFrames for each classification group.
    """

    logger.info("Classifying rows...")
    merge_col = config['merge_indicator']
    status = config['merge_status']
    labels = config['result_labels']

    # Matched
    match_cond = merged[merge_col] == status['both']
    for pair in config['comparison_pairs']:
        left_col = f"{pair['base']}{pair['suffixes'][0]}"
        right_col = f"{pair['base']}{pair['suffixes'][1]}"
        match_cond &= (merged[left_col] == merged[right_col])
    matched = merged[match_cond].copy()
    matched['result'] = labels['matched']

    # Only internal
    only_internal = merged[merged[merge_col] == status['left_only']].copy()
    only_internal['result'] = labels['only_internal']

    # Only provider
    only_provider = merged[merged[merge_col] == status['right_only']].copy()
    only_provider['result'] = labels['only_provider']

    # Mismatched
    mismatch_cond = merged[merge_col] == status['both']
    mismatch_pairs = []
    for pair in config['comparison_pairs']:
        left_col = f"{pair['base']}{pair['suffixes'][0]}"
        right_col = f"{pair['base']}{pair['suffixes'][1]}"
        mismatch_pairs.append(merged[left_col] != merged[right_col])
    if mismatch_pairs:
        mismatch_total = mismatch_pairs[0]
        for cond in mismatch_pairs[1:]:
            mismatch_total |= cond
        mismatch_cond &= mismatch_total
    mismatched = merged[mismatch_cond].copy()
    mismatched['result'] = labels['mismatched']

    logger.info(f"Matched: {matched.shape[0]}, Only Internal: {only_internal.shape[0]}, "
                f"Only Provider: {only_provider.shape[0]}, Mismatched: {mismatched.shape[0]}")

    return {
        'matched': matched,
        'only_internal': only_internal,
        'only_provider': only_provider,
        'mismatched': mismatched
    }