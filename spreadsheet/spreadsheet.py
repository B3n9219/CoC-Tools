from settings import *
import utilities as util

import os
import re

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib  .flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_credentials():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    return credentials


creds = get_credentials()
service = build("sheets", "v4", credentials=creds)
sheets = service.spreadsheets()


def update_cell(cell,text,sheet):
    fullCell = f"{sheet}!{cell}"
    try:
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=fullCell
                           , valueInputOption="USER_ENTERED", body={"values": [[text]]}).execute()
        print(f"{text} added to cell {fullCell}")
    except HttpError as error:
        print(error)


def batch_update_cells(cellRange, textList, sheet):
    fullRange = f"{sheet}!{cellRange}"
    try:
        # Extract the start and end cells from the range
        match = re.match(r'([A-Za-z]+)(\d+):([A-Za-z]+)(\d+)', cellRange)
        if not match:
            raise ValueError("Invalid range format. Example of valid format: A1:A10 or A1:F1")

        start_column, start_row, end_column, end_row = match.groups()
        start_row, end_row = int(start_row), int(end_row)

        # Determine if the range spans multiple columns or just a single column
        if start_row == end_row:  # Single row, multiple columns
            row_range = f"{sheet}!{start_column}{start_row}:{end_column}{end_row}"
            values = [textList]  # List of values for the row
        else:  # Multiple rows, single column
            row_range = f"{sheet}!{start_column}{start_row}:{end_column}{end_row}"
            values = [[text] for text in textList]  # Each value in its own row

        # Prepare the batch update request body
        batch_update_values_request_body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": row_range, "values": values}
            ],
        }

        # Execute the batch update
        sheets.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=batch_update_values_request_body
        ).execute()

        print(f"Updated cells {fullRange}")
    except HttpError as error:
        print(f"An error occurred: {error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def read_range(cellRange, sheet):
    fullRange = f"{sheet}!{cellRange}"
    try:
        result = (
            sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=fullRange).execute()
        )
        if "values" in result:
            rows = result["values"]
            #print(f"{len(rows)} rows retrieved from cell range {fullRange}")
            # Flatten the list of lists into a single list
            result = [word for sublist in rows for word in sublist]
        else:
            # If "values" key is missing, it means the range is empty
            print(f"No values found in the range {fullRange}")
            result = []
        return result

    except HttpError as error:
        print(error)


def get_sheet_id_by_name(sheet_name):
    # Get spreadsheet metadata
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()

    # Iterate through sheets to find the matching sheet name
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']

    raise ValueError(f"Sheet with name '{sheet_name}' not found.")

def merge_cells(start_row, end_row, start_column, end_column, sheet_name):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    sheet_id = get_sheet_id_by_name(sheet_name)
    # Define the merge request
    merge_request = {
        'requests': [
            {
                'mergeCells': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': start_row,
                        'endRowIndex': end_row,
                        'startColumnIndex': start_column,
                        'endColumnIndex': end_column
                    },
                    'mergeType': 'MERGE_ALL'
                }
            }
        ]
    }
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=merge_request)
    response = request.execute()

    print(f"Cells merged in sheet ID {sheet_id}, range {start_row}:{end_row} - {start_column}:{end_column}")


