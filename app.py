import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -------------------------
# STEP 1: Google Sheet সংযোগ সেটআপ
# -------------------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)

# তোমার শিটের URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1TidiwlJn929qZHlU32tcyWoJMObTpIKjBbuUGp0oEqM/edit?gid=0#gid=0"
sheet = client.open_by_url(SHEET_URL).sheet1

# -------------------------
# STEP 2: ইনপুট ডেটা নেওয়া
# -------------------------
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

# -------------------------
# STEP 3: শিটে ডেটা যোগ করা
# -------------------------
# স্বয়ংক্রিয়ভাবে SL নম্বর তৈরি
last_row = len(sheet.get_all_values())
sl_no = last_row  # ধরছি প্রথম রো হেডার

data = [sl_no, date, designer, buyer, job, machine, item, ups, color, set_, plate, impression, qty, comment]

sheet.append_row(data)

print("✅ ডেটা সফলভাবে Google Sheet-এ যুক্ত হয়েছে!")
