import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

# ---------------------------------
# 🔹 Google Credentials Setup
# ---------------------------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def get_google_sheet_connection():
    try:
        # Try Streamlit secrets first
        if 'gcp_service_account' in st.secrets:
            CREDS = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], 
                scopes=SCOPE
            )
            st.success("✅ Credentials loaded from Streamlit secrets")
        else:
            # Fallback to credentials.json for local development
            CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
            st.success("✅ Credentials loaded from local file")
        
        CLIENT = gspread.authorize(CREDS)
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        SHEET = CLIENT.open_by_key(SHEET_ID).sheet1
        
        # Test connection
        SHEET.get_all_records()
        st.success("✅ Successfully connected to Google Sheet")
        return SHEET
        
    except gspread.exceptions.APIError as e:
        st.error(f"🚫 Google Sheets API Error: {e}")
        st.info("Please ensure:")
        st.info("1. Google Sheets API is enabled in Google Cloud Console")
        st.info("2. Service account has editor access to the sheet")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("🚫 Spreadsheet not found. Please check the SHEET_ID")
        return None
    except Exception as e:
        st.error(f"🚫 Unexpected error: {e}")
        return None

# Initialize connection
SHEET = get_google_sheet_connection()

if SHEET is None:
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
                data[f] = st.number_input(f, min_value=0, step=1, value=0)
            else:
                data[f] = st.text_input(f, value="")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    # Validate required fields
    required_fields = ["Designer Name", "Item Name", "Qty"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        st.error(f"❌ Please fill in required fields: {', '.join(missing_fields)}")
    else:
        try:
            new_row = [data[f] for f in FIELDS]
            new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            SHEET.append_row(new_row)
            st.success("✅ Data successfully added to Google Sheet!")
            st.balloons()
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
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download CSV", 
                df.to_csv(index=False), 
                "sheet_data.csv",
                "text/csv"
            )
        with col2:
            st.write(f"**Total Records:** {len(df)}")
    else:
        st.info("📝 No records found in the sheet. Add your first record above!")
        
except Exception as e:
    st.warning(f"⚠️ Couldn't load data from Google Sheet: {e}")
