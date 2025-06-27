"""
------------------------------------------------------------------------------
Streamlit Web App for Mini Reconciliation Tool

This app provides a user-friendly interface to reconcile transactions between
an internal system export and a payment provider statement.

Key Features:
  - Allows users to upload two CSV files with required columns.
  - Validates file structure immediately upon upload.
  - Runs the full reconciliation workflow using the backend Reconciler class.
  - Displays results in four clear categories:
      1) Matched Transactions
      2) Only in Internal
      3) Only in Provider
      4) Mismatched rows (optional)
  - Enables users to download each result set as a CSV.
  - Supports a clear "start over" reset button.

This front end makes the core reconciliation logic accessible to non-technical
users through a simple browser interface.
------------------------------------------------------------------------------
"""

import streamlit as st
import pandas as pd
from src.mini_reconcile.core.reconciler import Reconciler

st.set_page_config(page_title="Mini Reconciliation Tool", layout="wide")
st.title("📊 Mini Reconciliation Tool")

REQUIRED_COLUMNS = ["transaction_reference", "amount", "status"]

st.markdown(
    "ℹ️ **How it works**\n\n"
    "- Upload **two CSV files**:\n\n"
    "  1️⃣ *Internal System Export*  \n"
    "  2️⃣ *Provider Statement*  \n"
    "- Each file **must include these columns**:\n"
    f"  - {', '.join(f'`{col}`' for col in REQUIRED_COLUMNS)}\n"
    "- File must be **comma-separated**, **not empty**, and **UTF-8 encoded**."
)

# === Session state ===
if "df_internal" not in st.session_state:
    st.session_state.df_internal = None
if "df_provider" not in st.session_state:
    st.session_state.df_provider = None
if "results" not in st.session_state:
    st.session_state.results = None


# === Validation function ===
def validate_file(file, label):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        st.error(
            f"🚫 The **{label}** file could not be read. "
            f"Please upload a valid CSV. Error: {e}"
        )
        return None

    if df.empty:
        st.error(f"⚠️ The **{label}** file is empty.")
        return None

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        st.error(
            f"⚠️ The **{label}** file is missing required column(s): "
            f"{', '.join(f'`{col}`' for col in missing_cols)}"
        )
        st.info(
            f"✅ Expected columns: "
            f"{', '.join(f'`{col}`' for col in REQUIRED_COLUMNS)}"
        )
        return None

    st.success(f"✅ {label} file looks good! ({df.shape[0]} rows)")
    return df


# === Upload widgets ===
internal_file = st.file_uploader(
    "Upload Internal System CSV", type=["csv"], key="internal_upload"
)
provider_file = st.file_uploader(
    "Upload Provider Statement CSV", type=["csv"], key="provider_upload"
)


# === Validate immediately ===
if internal_file:
    valid_internal = validate_file(internal_file, "Internal System Export")
    st.session_state.df_internal = valid_internal

if provider_file:
    valid_provider = validate_file(provider_file, "Provider Statement")
    st.session_state.df_provider = valid_provider


# === Submit button (inside form) ===
with st.form("run_form"):
    submitted = st.form_submit_button("Run Reconciliation")
    if submitted:
        if st.session_state.df_internal is not None and st.session_state.df_provider is not None:
            reconciler = Reconciler()
            try:
                results = reconciler.reconcile(
                    st.session_state.df_internal,
                    st.session_state.df_provider
                )
                st.session_state.results = results
            except Exception as e:
                st.error("🚫 Oops, something went wrong during reconciliation.")
                st.exception(e)
        else:
            st.warning("⚠️ Please fix the file issues above before running reconciliation.")


# === Show results ===
if st.session_state.results:
    for label, emoji in {
        "matched": "✅ Matched Transactions",
        "only_internal": "⚠️ Only in Internal",
        "only_provider": "❌ Only in Provider",
        "mismatched": "🔍 Mismatched",
    }.items():
        df = st.session_state.results[label]
        st.subheader(f"{emoji} ({len(df)})")
        st.dataframe(df)
        st.download_button(
            "Download",
            df.to_csv(index=False),
            file_name=f"{label}.csv",
            key=f"{label}_dl"
        )

    if st.button("Clear all & start over"):
        st.session_state.df_internal = None
        st.session_state.df_provider = None
        st.session_state.results = None
        st.rerun()
