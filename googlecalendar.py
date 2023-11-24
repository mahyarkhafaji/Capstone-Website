import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pytz
import openpyxl, os
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import backoff
import time
from googleapiclient.http import MediaFileUpload

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
    
    
    #Weekly Folder
    weekCount = 1  # Keeps track of weeks
    currentWeek = 'Week 1'
    weekData = []  # Stores data for the current week
    service = build("drive", "v3", credentials=creds)

    for row in data[1:]:  # Skip the header row
        if (weekCount - 1) * 2 <= data.index(row) < weekCount * 2:
            weekData.append(row)
        else:
            # Process and upload the data for the completed week
            process_and_upload_week_data(service, currentWeek, weekData)

            # Prepare for the next week
            weekCount += 1
            currentWeek = 'Week ' + str(weekCount)
            weekData = [row]
            # Process and upload the last week's data
    if weekData:
        process_and_upload_week_data(service, currentWeek, weekData)


  except HttpError as error:
    print(f"An error occurred: {error}")


def process_and_upload_week_data(service, weekName, weekData):
    # Define your labels here, matching the structure of your Excel data
    labels = ["Date", "Lecture Number", "Lab Number", "", "Topic", "Reading", "HW Number", "HW Number Due", "Lab Number Due"]

    # Create a folder for the week
    weekFolderId = create_folder(service, weekName, get_folder_id("IT212-New", service))
    
    # Create a text file with the week's data
    weekFileName = f"{weekName}_info.txt"
    with open(weekFileName, 'w') as file:
        for row in weekData:
            labeled_row = [f"{label}: {data}" for label, data in zip(labels, row)]
            file.write(', '.join(labeled_row) + '\n')
    
    # Upload the file to Google Drive
    upload_file_to_drive(service, weekFolderId, weekFileName)

def write_to_file(filename, data):
    """Write or append data to a local text file."""
    with open(filename, 'a') as file:
        file.write(data + '\n')

def upload_file_to_drive(service, folder_id, filename):
    """Upload a file to Google Drive."""
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='text/plain')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

#Get folder ID
def get_folder_id(folder_name, service):
    # Query to search for folders with the specified name
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}' and trashed = false"
    print(f"Query: {query}")  # Debugging: Print the query to check its correctness
    try:
        response = service.files().list(q=query, fields='files(id, name)').execute()
        folders = response.get('files', [])
        if not folders:
            print("No folders found.")
            return None
        else:
            # Assuming the first folder in the list is the one you're looking for
            return folders[0].get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

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

#def create_and_upload_file(service, folder_id, title, content, mimeType):
 #   file_metadata = {'name': title, 'parents': [folder_id], 'mimeType': mimeType}
    # Add logic to handle file content if necessary
  #  file = service.files().create(body=file_metadata, fields='id').execute()
   # print(f"Created file {title} with ID: {file.get('id')}")


#Get file ID
def get_id(fname, service, folder_id):
    # Query to search for files with the specified name in the specified folder
    query = f"name = '{fname}' and '{folder_id}' in parents and trashed = false"
    try:
        response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = response.get('files', [])
        if not files:
            print("No files found.")
            return None
        else:
            # Assuming the first file in the list is the one you're looking for
            return files[0].get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def create_folder(service, folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive.

    Args:
    service: Authorized Google Drive service instance.
    folder_name: The name of the folder to create.
    parent_folder_id: The ID of the parent folder (optional).

    Returns:
    The ID of the created folder.
    """
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    # If a parent folder ID is provided, add it to the folder's metadata
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]

    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
        return folder.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == "__main__":
  main()