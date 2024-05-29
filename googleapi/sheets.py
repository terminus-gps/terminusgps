from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_imeis(
    spreadsheet_id: str,
    range_name: str,
    creds: Credentials,
) -> list[str]:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    )
    values = result.get("values", [])

    if not values:
        raise ValueError("No data found.")

    return [row[0] for row in values]
