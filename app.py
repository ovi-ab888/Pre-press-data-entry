import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

# Google Sheets setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
CLIENT = gspread.authorize(CREDS)

# Google Sheet ID (replace with your own)
SHEET_ID = "YOUR_SHEET_ID_HERE"
SHEET = CLIENT.open_by_key(SHEET_ID).sheet1

# Define form fields
FIELDS = [
    "Designer Name",
    "Buyer",
    "Job",
    "Machine",
    "Item Name",
    "UPS",
    "Color",
    "Set",
    "Plate",
    "Impression",
    "Qty"
]

st.subheader("Enter New Record")

# Two-column layout form
with st.form("entry_form"):
    cols = st.columns(2)
    form_data = {}
    for i, field in enumerate(FIELDS):
        with cols[i % 2]:
            if field == "Qty":
                form_data[field] = st.number_input(field, min_value=0, step=1)
            else:
                form_data[field] = st.text_input(field)
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    if not form_data["Designer Name"] or not form_data["Item Name"]:
        st.error("⚠️ Please fill at least 'Designer Name' and 'Item Name'")
    else:
        new_row = [form_data[f] for f in FIELDS]
        new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        SHEET.append_row(new_row)
        st.success("✅ Data successfully added to Google Sheet!")

# Display existing data
st.markdown("---")
st.subheader("📊 Existing Records")
try:
    records = SHEET.get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), "sheet_data.csv")
    else:
        st.info("No records found in the sheet.")
except Exception as e:
    st.error(f"Unable to load data: {e}")
