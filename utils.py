import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key("your_google_sheet_id_here").worksheet(sheet_name)

def append_row(sheet_name, data):
    sheet = get_sheet(sheet_name)
    sheet.append_row(data)

def search_by_column(sheet_name, col_index, keyword):
    sheet = get_sheet(sheet_name)
    values = sheet.get_all_values()
    results = [row for row in values if row[col_index].strip() == keyword]
    return results
