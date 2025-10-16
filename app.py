import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from pathlib import Path

# ---------------------------
# App setup
# ---------------------------
st.set_page_config(page_title="Prepress Data Entry", layout="wide")
st.title("🧾 Google Sheet (CSV) Data Entry Form")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
LOCAL_CSV = DATA_DIR / "entries.csv"

# 👉 তোমার Published Google Sheet CSV লিংক এখানে বসাও
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQTcDBYH733mtxPq9WnWm2J-WCNCkd9TKQMtxHeh1XPjiM_kDpkVZutjwo9bewfJ1cyF3PnkWLPuhl9/pub?gid=0&single=true&output=csv"

# ---------------------------
# Form fields
# ---------------------------
FIELDS = [
    "Designer Name", "Buyer", "Job", "Machine", "Item Name",
    "UPS", "Color", "Set", "Plate", "Impression", "Qty"
]

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Enter New Record")

    with st.form("entry_form"):
        cols = st.columns(2)
        inputs = {}
        for i, field in enumerate(FIELDS):
            with cols[i % 2]:
                if field == "Qty":
                    inputs[field] = st.number_input(field, min_value=0, step=1)
                else:
                    inputs[field] = st.text_input(field)

        submitted = st.form_submit_button("Save Locally")

    if submitted:
        row = {f: inputs[f] for f in FIELDS}
        row["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_row = pd.DataFrame([row])
        if LOCAL_CSV.exists():
            df_row.to_csv(LOCAL_CSV, mode="a", header=False, index=False)
        else:
            df_row.to_csv(LOCAL_CSV, index=False)
        st.success("✅ Data saved locally (not in Google Sheet).")

# ---------------------------
# Display Google Sheet (Published CSV)
# ---------------------------
with col2:
    st.subheader("📊 Data from Published Google Sheet")
    try:
        df = pd.read_csv(CSV_URL)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download Sheet CSV", df.to_csv(index=False), "google_sheet.csv")
    except Exception as e:
        st.error(f"❌ Failed to load published Google Sheet CSV:\n\n{e}")

# ---------------------------
# Optional: Local entries viewer
# ---------------------------
st.markdown("---")
st.subheader("📁 Locally Saved Entries")
if LOCAL_CSV.exists():
    df_local = pd.read_csv(LOCAL_CSV)
    st.dataframe(df_local, use_container_width=True)
    st.download_button("⬇️ Download Local Entries", df_local.to_csv(index=False), "entries_local.csv")
else:
    st.info("No local entries yet.")
