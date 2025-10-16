import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Debug Connection", layout="wide")
st.title("🔧 Connection Debugger")

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

def debug_connection():
    st.subheader("Step 1: Check Secrets")
    try:
        secrets = st.secrets["gcp_service_account"]
        st.success("✅ Secrets loaded successfully")
        
        # Display key info (masked)
        st.write(f"**Project ID:** {secrets['project_id']}")
        st.write(f"**Client Email:** {secrets['client_email']}")
        st.write(f"**Private Key ID:** {secrets['private_key_id'][:10]}...")
        st.write(f"**Private Key Length:** {len(secrets['private_key'])} characters")
        
    except Exception as e:
        st.error(f"❌ Failed to load secrets: {e}")
        return False

    st.subheader("Step 2: Check Credentials")
    try:
        creds_dict = dict(secrets)
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        st.success("✅ Credentials created successfully")
    except Exception as e:
        st.error(f"❌ Failed to create credentials: {e}")
        return False

    st.subheader("Step 3: Check Authorization")
    try:
        client = gspread.authorize(credentials)
        st.success("✅ Client authorized successfully")
    except Exception as e:
        st.error(f"❌ Failed to authorize client: {e}")
        return False

    st.subheader("Step 4: Check Sheet Access")
    try:
        SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
        sheet = client.open_by_key(SHEET_ID).sheet1
        st.success("✅ Sheet accessed successfully")
        
        # Test read operation
        records = sheet.get_all_records()
        st.success(f"✅ Read test successful - Found {len(records)} records")
        return True
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Spreadsheet not found. Possible causes:")
        st.error("1. Wrong SHEET_ID")
        st.error("2. Service account doesn't have access to the sheet")
        st.error("3. Sheet doesn't exist")
        return False
    except gspread.exceptions.APIError as e:
        st.error(f"❌ API Error: {e}")
        st.error("This usually means permission issues")
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return False

# Run debug
if debug_connection():
    st.balloons()
    st.success("🎉 All tests passed! Your connection is working.")
else:
    st.error("🚫 Connection failed. Please check the errors above.")

st.markdown("---")
st.subheader("🔍 Quick Fixes")

st.write("""
**If you're getting permission errors:**

1. **Share the Google Sheet** with this email:
   `streamlit-sheet-app@infra-signifier-471306-e2.iam.gserviceaccount.com`

2. **Make sure sharing is correct:**
   - Open your Google Sheet
   - Click 'Share' button
   - Add the email above
   - Set permission to 'Editor'
   - Click 'Send'

3. **Wait a few minutes** after sharing for permissions to propagate

**If you're getting JWT signature errors:**
- This is usually a private key formatting issue
- Make sure the private key in secrets.toml has proper `\\n` characters
""")
