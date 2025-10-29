import os, json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
load_dotenv()

creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
print("✅ Credentials loaded:", creds["client_email"])
print("✅ Spreadsheet ID:", os.getenv("SPREADSHEET_ID"))


async def append_to_sheet(first_name, last_name, email, message):
    try:
        creds_json = os.getenv("GOOGLE_CREDENTIALS")
        if not creds_json:
            raise ValueError("GOOGLE_CREDENTIALS not found in environment variables")

        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        sheet.values().append(
            spreadsheetId=os.getenv("SPREADSHEET_ID"),
            range="A:D",
            valueInputOption="RAW",
            body={"values": [[first_name, last_name, email, message]]},
        ).execute()

        print("✅ Data successfully appended to sheet.")
        return True

    except Exception as e:
        print(f"❌ Error appending to sheet: {e}")
        return False
