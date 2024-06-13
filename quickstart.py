import os.path
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of SRABot tracker
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
ENV_SHEETID = os.getenv('ENV_SHEETID')
PROMPT_SHEETID = os.getenv('PROMPT_SHEETID')
DOCUMENT_SHEETID = os.getenv('DOCUMENT_SHEETID')


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("secrets/token.json"):
    creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("secrets/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheetNames = ['.env', 'Documents']

    docResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"Documents!A3:C").execute()
    envResult = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f".env!A3:D").execute()
    documents = docResult.get('values', "")
    env = envResult.get('values', "")
    print(documents)
    print(env)

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()