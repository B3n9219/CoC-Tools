from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib  .flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import re
import time

from config.config import config
from utilities.general_util import entire_column



SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/drive.file']

def get_credentials():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    project_dir = os.path.dirname(parent_dir)

    token_path = os.path.join(project_dir, os.path.join("creds", "token.json"))
    credentials_path = os.path.join(project_dir, os.path.join("creds", "credentials.json"))
    credentials = None
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(credentials.to_json())
    return credentials

def get_sheet_settings():
    setting_names = read_range(entire_column(config["setting_name_column"]), config["setting_sheet"])
    setting_values = read_range(entire_column(config["setting_value_column"]), config["setting_sheet"])
    return (setting_names, setting_values)


creds = get_credentials()
service = build("sheets", "v4", credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)
sheets = service.spreadsheets()


def update_cell(cell,text,sheet):
    fullCell = f"{sheet}!{cell}"
    try:
        sheets.values().update(spreadsheetId=config["sheet_id"], range=fullCell
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
            spreadsheetId=config["sheet_id"], body=batch_update_values_request_body
        ).execute()

        print(f"Updated cells {fullRange}")
    except HttpError as error:
        print(f"An error occurred: {error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def read_range(cellRange, sheet):
    fullRange = f"{sheet}!{cellRange}"
    retries = 3
    delay = 15
    for attempt in range(retries):
        try:
            result = (
                sheets.values().get(spreadsheetId=config["sheet_id"], range=fullRange).execute()
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
            if error.resp.status in [502, 503, 504]:  # Server-side issues
                print(f"Error {error.resp.status}: {error.content}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                # If it's a different error, re-raise it
                raise
    raise Exception(f"Failed to retrieve data from range {fullRange} after {retries} retries.")


def get_sheet_id_by_name(sheet_name):
    # Get spreadsheet metadata
    spreadsheet = service.spreadsheets().get(spreadsheetId=config["sheet_id"]).execute()

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
    request = service.spreadsheets().batchUpdate(spreadsheetId=config["sheet_id"], body=merge_request)
    response = request.execute()

    print(f"Cells merged in sheet ID {sheet_id}, range {start_row}:{end_row} - {start_column}:{end_column}")

def make_spreadsheet(sheet_title):
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        # Metadata for the new copy
        file_metadata = {
            'name': sheet_title,  # Title of the new spreadsheet
            'parents': [config["spreadsheet_folder_id"]],  # Folder ID where the new file should be placed
        }

        # Copy the template file
        copied_file = drive_service.files().copy(
            fileId=config["template_id"],
            body=file_metadata
        ).execute()

        copied_file_id = copied_file.get('id')

        # Make the new spreadsheet publicly accessible
        permission_body = {
            'type': 'anyone',
            'role': 'reader'  # Change to 'writer' if you want to allow editing
        }

        # Create the permission for the new file
        drive_service.permissions().create(
            fileId=copied_file_id,
            body=permission_body
        ).execute()

        # Print the new file ID
        print(f"Spreadsheet '{sheet_title}' made successfully! Spreadsheet ID: {copied_file_id}")
        print(f"The spreadsheet is now accessible at: https://docs.google.com/spreadsheets/d/{copied_file_id}/edit")

        return copied_file_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
