import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PEPCO Data Processor",
    page_icon="🏭",
    layout="centered"
)

# Title and description
st.title("🏭 PEPCO Data Processor")
st.markdown("### Monitrms Automation")
st.markdown("---")

# Google Sheets connection function
@st.cache_resource
def connect_gsheet():
    SCOPE = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    
    # Streamlit secrets theke credentials
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    
    # Your Google Sheet link use kore connection
    sheet = client.open_by_key("1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM").sheet1
    return sheet

def main():
    # Main data entry form
    with st.form("pepco_data_form", clear_on_submit=True):
        st.subheader("📝 Data Entry Form")
        
        # Two columns layout
        col1, col2 = st.columns(2)
        
        with col1:
            designer_name = st.text_input("*Designer Name", placeholder="Enter designer name")
            buyer = st.text_input("*Buyer", placeholder="Enter buyer name")
            job = st.text_input("*Job", placeholder="Job reference")
            machine = st.text_input("*Machine", placeholder="Machine name/number")
            item_name = st.text_input("*Item Name", placeholder="Item description")
        
        with col2:
            ups = st.text_input("*UPS", placeholder="UPS details")
            color = st.text_input("*Color", placeholder="Color information")
            set_field = st.text_input("*Set", placeholder="Set details")
            plate = st.text_input("*Plate", placeholder="Plate information")
            impression = st.text_input("*Impression", placeholder="Impression details")
        
        # Quantity input - full width
        qty = st.number_input("*Qty", min_value=1, value=1, step=1)
        
        # Additional notes (optional)
        comments = st.text_area("Additional Comments (Optional)", 
                               placeholder="Any additional notes...")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Data to Google Sheet")
        
        if submitted:
            # Validation - check required fields
            required_fields = [
                designer_name, buyer, job, machine, item_name,
                ups, color, set_field, plate, impression
            ]
            
            if not all(field.strip() for field in required_fields):
                st.error("❌ Please fill all required fields (*)")
            else:
                try:
                    # Connect to Google Sheet
                    sheet = connect_gsheet()
                    
                    # Prepare data for the sheet
                    row_data = [
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
                        designer_name.strip(),
                        buyer.strip(),
                        job.strip(),
                        machine.strip(),
                        item_name.strip(),
                        ups.strip(),
                        color.strip(),
                        set_field.strip(),
                        plate.strip(),
                        impression.strip(),
                        qty,
                        comments.strip() if comments else ""  # Comments
                    ]
                    
                    # Append to Google Sheet
                    sheet.append_row(row_data)
                    
                    # Success message
                    st.success("✅ Data successfully saved to Google Sheet!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error saving data: {str(e)}")

    # Data viewing section
    st.markdown("---")
    st.subheader("📊 Data Management")
    
    if st.button("🔄 Refresh Data View"):
        try:
            sheet = connect_gsheet()
            records = sheet.get_all_records()
            
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df.tail(10))  # Show last 10 entries
                st.info(f"Total entries: {len(records)}")
            else:
                st.info("No data found in the sheet yet.")
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    main()
