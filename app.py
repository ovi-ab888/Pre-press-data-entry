import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("🧾 Pre-Press Data Entry Form")

# Load credentials from Streamlit Secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = gspread.authorize(creds)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM/edit#gid=0"
sheet = client.open_by_url(SHEET_URL).sheet1

with st.form("data_entry_form"):
    designer = st.text_input("Designer Name")
    buyer = st.text_input("Buyer")
    job = st.text_input("Job")
    machine = st.text_input("Machine")
    item = st.text_input("Item Name")
    ups = st.text_input("UPS")
    color = st.text_input("Color")
    set_ = st.text_input("Set")
    plate = st.text_input("Plate")
    impression = st.text_input("Impression")
    qty = st.text_input("Quantity")
    comment = st.text_area("Comment")

    submitted = st.form_submit_button("Submit")

    if submitted:
        date = datetime.now().strftime("%Y-%m-%d")
        last_row = len(sheet.get_all_values())
        sl_no = last_row
        data = [sl_no, date, designer, buyer, job, machine, item, ups, color, set_, plate, impression, qty, comment]
        sheet.append_row(data)
        st.success("✅ Data successfully saved to Google Sheet!")
