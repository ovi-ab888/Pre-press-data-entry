import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

# Google Sheets API scope
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

def initialize_gsheet():
    """Initialize and return Google Sheet connection"""
    try:
        # Load credentials from Streamlit secrets
        creds_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(credentials)
        
        # Your Google Sheet ID
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        st.success("✅ Successfully connected to Google Sheets!")
        return sheet
        
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.info("""
        **Troubleshooting steps:**
        1. Check if service account has access to the Google Sheet
        2. Verify Google Sheets API is enabled
        3. Ensure credentials are correct in secrets.toml
        """)
        return None

# Initialize connection
SHEET = initialize_gsheet()

if SHEET is None:
    st.stop()

# Data Entry Form
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
    if SHEET:
        try:
            # Prepare data row
            new_row = [data[field] for field in FIELDS]
            new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Append to sheet
            SHEET.append_row(new_row)
            st.success("✅ Data successfully added to Google Sheet!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Failed to write data: {str(e)}")

# Display existing data
st.markdown("---")
st.subheader("📊 Existing Records")

if SHEET:
    try:
        records = SHEET.get_all_records()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    "sheet_data.csv",
                    "text/csv"
                )
            with col2:
                st.metric("Total Records", len(df))
        else:
            st.info("No records found. Add your first record above!")
            
    except Exception as e:
        st.warning(f"⚠️ Error loading data: {str(e)}")
