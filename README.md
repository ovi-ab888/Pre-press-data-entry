# 🧾 Pre-Press Data Entry Streamlit App

A simple Streamlit form app that saves form input data to a specific Google Sheet.

## 🚀 How to Run Locally

1. Clone the repo or unzip this project.
2. Create a file named `.streamlit/secrets.toml` and paste your Google Cloud credentials:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "YOUR_PROJECT_ID"
   private_key_id = "YOUR_PRIVATE_KEY_ID"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "YOUR_CLIENT_EMAIL"
   token_uri = "https://oauth2.googleapis.com/token"
   ```
3. Run the app:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Your data will automatically be saved to the linked Google Sheet.
