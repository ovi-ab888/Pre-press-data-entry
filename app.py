import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

# Google Sheets API scope
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def get_google_sheet():
    """Initialize and return Google Sheet connection"""
    try:
        st.info("🔄 Attempting to connect to Google Sheets...")
        
        # Method 1: Direct from secrets with proper key formatting
        secrets = st.secrets["gcp_service_account"]
        
        # Create credentials dictionary
        creds_dict = {
            "type": secrets["type"],
            "project_id": secrets["project_id"],
            "private_key_id": secrets["private_key_id"],
            "private_key": secrets["private_key"],
            "client_email": secrets["client_email"],
            "client_id": secrets["client_id"],
            "auth_uri": secrets["auth_uri"],
            "token_uri": secrets["token_uri"],
            "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": secrets["client_x509_cert_url"],
            "universe_domain": secrets["universe_domain"]
        }
        
        st.write("✅ Credentials loaded from secrets")
        
        # Create credentials
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(credentials)
        
        st.write("✅ Google Sheets client authorized")
        
        # Your Google Sheet ID
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        st.write("✅ Google Sheet accessed successfully")
        
        # Test connection by getting records
        records = sheet.get_all_records()
        st.write(f"✅ Connection test successful. Found {len(records)} records")
        
        return sheet
        
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.error(f"❌ Error type: {type(e).__name__}")
        return None

# Initialize connection
SHEET = get_google_sheet()

if SHEET is None:
    st.error("""
    🚫 **Critical Connection Issue**
    
    **Possible Solutions:**
    1. **Check Sheet Sharing**: Ensure this email is added as Editor to your Google Sheet:
       `streamlit-sheet-app@infra-signifier-471306-e2.iam.gserviceaccount.com`
    
    2. **Enable Google Sheets API**:
       - Go to [Google Cloud Console](https://console.cloud.google.com/)
       - Select your project
       - Go to **APIs & Services > Library**
       - Search for "Google Sheets API" and enable it
    
    3. **Check Service Account**:
       - Go to **IAM & Admin > Service Accounts**
       - Ensure the service account is active
    
    4. **Verify Secrets Format**:
       - Ensure private key has proper `\\n` formatting
    """)
    st.stop()

# Rest of your app code...
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

if submitted and SHEET:
    try:
        new_row = [data[field] for field in FIELDS]
        new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        SHEET.append_row(new_row)
        st.success("✅ Data successfully added to Google Sheet!")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Failed to write data: {str(e)}")

# Display existing data
if SHEET:
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
