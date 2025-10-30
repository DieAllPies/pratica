import os
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# ============================
# Load .env only for local runs
# (Cloud Run already injects variables)
# ============================
if os.getenv("ENV") != "cloud":
    load_dotenv()

# ============================
# Handle credentials
# ============================
creds_json = os.getenv("GOOGLE_CREDENTIALS")
spreadsheet_id = os.getenv("SPREADSHEET_ID")

if creds_json:
    try:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        print("✅ Google credentials loaded successfully.")
    except Exception as e:
        creds = None
        print(f"⚠️ Failed to parse credentials: {e}")
else:
    creds = None
    print("⚠️ No GOOGLE_CREDENTIALS found — Sheets disabled in this environment.")

# ============================
# Append function
# ============================
async def append_to_sheet(first_name, last_name, email, message):
    """Append a contact message to Google Sheets (works locally & on Cloud)."""
    try:
        if not creds:
            print("⚠️ Running locally without Sheets — skipping upload.")
            return True  # Simulate success to avoid crashes

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range="A:D",
            valueInputOption="RAW",
            body={"values": [[first_name, last_name, email, message]]},
        ).execute()

        print("✅ Data successfully appended to sheet.")
        return True

    except Exception as e:
        print(f"❌ Error appending to sheet: {e}")
        return False
