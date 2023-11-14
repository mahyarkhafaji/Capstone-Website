import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pytz
import openpyxl, os
#from docx import Document
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
#from Google import Create_Service
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import numpy as np
import backoff
import time

def format_date(date):
    x = date.split('/')
    return datetime(2024, int(x[0]), int(x[1]), 13, 0, 0)


# Define scopes
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/drive"]

# Main function
@backoff.on_exception(backoff.expo, HttpError, max_tries=5, giveup=lambda e: e.resp.status not in [429, 500, 503])
def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secrets.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:

#Authorize the API
    file_name = 'D:/XAMPP/htdocs/Web/client_service.json'
    service = build("calendar", "v3", credentials=creds)
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, SCOPES)
    client = gspread.authorize(creds)

#Fetch the sheet
    worksheet = client.open('IT212_Schedule').sheet1
    data = worksheet.get_all_values()
    # Parse through worksheet to manipulate cells
    for row in data[1:]:  # Skip header row
        date, event_description, homework, lab = row[0], row[4], row[7], row[8]
        if date:
            start_time = format_date(date)
            end_time = start_time + timedelta(hours=2)
            timezone = 'America/New_York'

        # Create and insert events
        events = []
        if event_description:
            events.append(create_event('Class', 'EnGeo 2209', event_description, start_time, end_time, timezone))
        if homework:
            events.append(create_event(f'HW {homework} due', 'EnGeo 2209', 'Homework', start_time, end_time, timezone))
        if lab:
            events.append(create_event(f'Lab {lab} due', 'EnGeo 2209', event_description, start_time, end_time, timezone))
            
        for event in events:
            service.events().insert(calendarId='dummytest12313@gmail.com', body=event).execute()
            time.sleep(1)  # Throttle requests to avoid quota limits

  except HttpError as error:
    print(f"An error occurred: {error}")

def create_event(summary, location, description, start_time, end_time, timezone):
    return {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

if __name__ == "__main__":
  main()