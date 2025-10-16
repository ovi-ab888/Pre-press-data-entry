import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Google Sheet Data Entry", layout="wide")
st.title("🧾 Google Sheet Data Entry Form")

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

def connect_to_sheets():
    try:
        # Load credentials
        secrets = st.secrets["gcp_service_account"]
        
        # Verify email domain
        if "lam.gserviceaccount.com" in secrets["client_email"]:
            st.error("❌ WRONG EMAIL DOMAIN: 'lam.gserviceaccount.com' found!")
            st.error("Please use 'iam.gserviceaccount.com' in your secrets.toml")
            return None
        
        # Create credentials
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
        
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(credentials)
        
        # Access sheet
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Test connection
        sheet.get_all_records()
        return sheet
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Sheet not found. Please check:")
        st.error("1. Sheet ID is correct")
        st.error("2. Service account is shared as Editor")
        st.error(f"3. Shared with: {secrets['client_email']}")
        return None
    except gspread.exceptions.APIError as e:
        st.error(f"❌ API Error: {e}")
        st.error("Please check Google Sheets API is enabled")
        return None
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        return None

# Initialize connection
with st.spinner("🔄 Connecting to Google Sheets..."):
    SHEET = connect_to_sheets()

if SHEET:
    st.success("✅ Successfully connected to Google Sheets!")
    
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
        try:
            new_row = [data[field] for field in FIELDS]
            new_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            SHEET.append_row(new_row)
            st.success("✅ Data successfully added to Google Sheet!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Failed to write data: {e}")

    # Display data
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
        st.warning(f"⚠️ Error loading data: {e}")

else:
    st.error("""
    🚫 **Connection Failed - Critical Issues:**
    
    1. **Email Domain Wrong**: You have 'lam.gserviceaccount.com' instead of 'iam.gserviceaccount.com'
    2. **Private Key Format**: Base64 padding error in private key
    
    **Quick Fix:**
    - Update secrets.toml with correct email domain
    - Use triple quotes for private key
    - Share sheet with correct email: `auto-generated@infra-signifier-471306-e2.iam.gserviceaccount.com`
    """)
