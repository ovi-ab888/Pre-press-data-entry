import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheet সংযোগ সেটআপ
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)

# তোমার Google Sheet এর URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM/edit#gid=0"
sheet = client.open_by_url(SHEET_URL).sheet1

# ইনপুট নেওয়া
print("🧾 Pre-press Data Entry")
date = datetime.now().strftime("%Y-%m-%d")
designer = input("Designer Name: ")
buyer = input("Buyer: ")
job = input("Job: ")
machine = input("Machine: ")
item = input("Item Name: ")
ups = input("UPS: ")
color = input("Color: ")
set_ = input("Set: ")
plate = input("Plate: ")
impression = input("Impression: ")
qty = input("Quantity: ")
comment = input("Comment: ")

# SL auto generate
last_row = len(sheet.get_all_values())
sl_no = last_row  # হেডার বাদে row count হিসেবে নিচ্ছি

data = [sl_no, date, designer, buyer, job, machine, item, ups, color, set_, plate, impression, qty, comment]

sheet.append_row(data)
print("✅ ডেটা সফলভাবে Google Sheet-এ যুক্ত হয়েছে!")
