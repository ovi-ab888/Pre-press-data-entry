import streamlit as st
import base64

st.title("🔧 Simple Credentials Test")

st.subheader("1. Checking Secrets Format")
try:
    secrets = st.secrets["gcp_service_account"]
    st.success("✅ Secrets loaded successfully")
    
    st.write(f"**Email:** {secrets['client_email']}")
    st.write(f"**Project:** {secrets['project_id']}")
    st.write(f"**Private Key Length:** {len(secrets['private_key'])} chars")
    
    # Check if email has correct domain
    if "iam.gserviceaccount.com" in secrets['client_email']:
        st.success("✅ Email domain is correct")
    else:
        st.error("❌ Email domain is incorrect")
        
except Exception as e:
    st.error(f"❌ Secrets error: {e}")

st.subheader("2. Testing Base64 Padding")
try:
    from google.oauth2.service_account import Credentials
    
    creds_dict = dict(st.secrets["gcp_service_account"])
    credentials = Credentials.from_service_account_info(creds_dict)
    st.success("✅ Credentials created successfully - No padding error!")
    
except Exception as e:
    st.error(f"❌ Credentials error: {e}")
    st.error("This is usually a private key formatting issue")
