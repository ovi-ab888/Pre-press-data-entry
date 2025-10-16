import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

# ---------------------------------
# 🔹 Google Credentials Setup (works both locally & on Streamlit Cloud)
# ---------------------------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    # if running on Streamlit Cloud with secrets
    CREDS = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
except Exception:
    # fallback for local run (with credentials.json)
    try:
        CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
    except Exception as e:
        st.error("❌ Couldn't load credentials. Please check credentials.json or Streamlit secrets.")
        st.stop()

# ---------------------------------
# 🔹 Try connecting to Google Sheet
# ---------------------------------
try:
    CLIENT = gspread.authorize(CREDS)
    SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"   # <-- replace with your sheet ID (not CSV link)
    SHEET = CLIENT.open_by_key(SHEET_ID).sheet1
except Exception as e:
    st.error("🚫 Couldn't connect to Google Sheet. Possible causes:\n"
             "- Wrong SHEET_ID\n"
             "- Service account not shared as Editor\n"
             "- Google Sheets API not enabled\n\n"
             f"**Detailed error:** {e}")
    st.stop()

# ---------------------------------
# 🔹 Data Entry Form
# ---------------------------------
FIELDS = [
    "Designer Name", "Buyer", "Job", "Machine", "Item Name",
    "UPS", "Color", "Set", "Plate", "Impression", "Qty"
]

st.subheader("Enter New Record")

with st.form("entry_form"):
    cols = st.columns(2)
    data = {}
    for i, f in enumerate(FIELDS):
        with cols[i % 2]:
            if f == "Qty":
                data[f] = st.number_input(f, min_value=0, step=1)
            else:
                data[f] = st.text_input(f)
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        new_row = [data[f] for f in FIELDS]
        new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        SHEET.append_row(new_row)
        st.success("✅ Data successfully added to Google Sheet!")
    except Exception as e:
        st.error(f"❌ Failed to write to Google Sheet: {e}")

# ---------------------------------
# 🔹 Display existing data
# ---------------------------------
st.markdown("---")
st.subheader("📊 Existing Records")

try:
    records = SHEET.get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), "sheet_data.csv")
    else:
        st.info("No records yet.")
except Exception as e:
    st.warning(f"⚠️ Couldn't load data from Google Sheet: {e}")
