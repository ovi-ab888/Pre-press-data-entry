import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("🔧 Connection Test - NEW SERVICE ACCOUNT")

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    st.write("📋 Step 1: Loading credentials...")
    secrets = st.secrets["gcp_service_account"]
    st.success("✅ Secrets loaded")
    st.write(f"Client Email: {secrets['client_email']}")
    
    st.write("🔑 Step 2: Creating credentials...")
    creds_dict = dict(secrets)
    credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    st.success("✅ Credentials created")
    
    st.write("🚀 Step 3: Authorizing client...")
    client = gspread.authorize(credentials)
    st.success("✅ Client authorized")
    
    st.write("📊 Step 4: Accessing sheet...")
    SHEET_ID = "1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM"
    sheet = client.open_by_key(SHEET_ID).sheet1
    st.success("✅ Sheet accessed")
    
    st.write("📖 Step 5: Testing read operation...")
    records = sheet.get_all_records()
    st.success(f"✅ Read successful - {len(records)} records found")
    
    st.balloons()
    st.success("🎉 ALL TESTS PASSED! Connection is working perfectly.")
    
except Exception as e:
    st.error(f"❌ Failed: {e}")
