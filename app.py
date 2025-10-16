import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def get_google_sheet():
    try:
        secrets = st.secrets["gcp_service_account"]
        creds_dict = dict(secrets)
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(credentials)
        
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Test connection
        sheet.get_all_records()
        return sheet
        
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        return None

SHEET = get_google_sheet()

if SHEET:
    st.success("✅ Successfully connected to Google Sheets!")
    
    FIELDS = [
        "Designer Name", "Buyer", "Job", "Machine", "Item Name",
        "UPS", "Color", "Set", "Plate", "Impression", "Qty"
    ]

    st.subheader("Enter New Record")
    with st.form("entry_form"):
        cols = st.columns(2)
        data = {}
        for i, field in enumerate(FIELDS):
            with cols[i % 2]:
                if field == "Qty":
                    data[field] = st.number_input(field, min_value=0, step=1, value=0)
                else:
                    data[field] = st.text_input(field, value="")
        submitted = st.form_submit_button("Submit Data")

    if submitted:
        try:
            new_row = [data[field] for field in FIELDS]
            new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            SHEET.append_row(new_row)
            st.success("✅ Data successfully added to Google Sheet!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Failed to write data: {str(e)}")

    st.markdown("---")
    st.subheader("📊 Existing Records")
    try:
        records = SHEET.get_all_records()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 Download CSV", df.to_csv(index=False), "sheet_data.csv", "text/csv")
        else:
            st.info("📝 No records found. Add your first record above!")
    except Exception as e:
        st.warning(f"⚠️ Error loading data: {str(e)}")
else:
    st.error("🚫 Could not connect. Please check sheet sharing.")
