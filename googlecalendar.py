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
    date_obj = datetime.strptime(date, '%Y-%m-%d')

    # Return a new datetime object with the specific time set (e.g., 13:00)
    return datetime(date_obj.year, date_obj.month, date_obj.day, 13, 0, 0)

#def get_week_number(date_str):
#    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#    return date_obj.isocalendar()[1]  # returns week number

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
    service2 = build("calendar", "v3", credentials=creds)
    service = build("drive", "v3", credentials=creds)
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, SCOPES)
    client = gspread.authorize(creds)

#Fetch the sheet
    worksheet = client.open('schedule').sheet1
    data = worksheet.get_all_values()
    # Parse through worksheet to manipulate cells
    for row in data[1:]:  # Skip header row
        date, event_description, homework, lab, discussion, quiz, exam = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        if date:
            start_time = format_date(date)
            end_time = start_time + timedelta(hours=2)
            timezone = 'America/New_York'

        # Create and insert events
        events = []
        if event_description:
            events.append(create_event('Class', 'EnGeo 2209', event_description, start_time, end_time, timezone))
        if homework:
            events.append(create_event(f'HW {homework} due', 'EnGeo 2209', 'Office Hours at Wednesdays 11:00 AM-1:00 PM', start_time, end_time, timezone))
        if lab:
            events.append(create_event(f'Lab {lab} due', 'EnGeo 2209', 'Office Hours at Wednesdays 11:00 AM-1:00 PM', start_time, end_time, timezone))
        if discussion:
            events.append(create_event(f'Discussion {discussion} due', 'EnGeo 2209', event_description, start_time, end_time, timezone))
        if quiz:
            events.append(create_event(f'Quiz {quiz} due', 'EnGeo 2209', 'Office Hours at Wednesdays 11:00 AM-1:00 PM', start_time, end_time, timezone))
        if exam:
            events.append(create_event(f'Exam {exam} due', 'EnGeo 2209', 'Office Hours at Wednesdays 11:00 AM-1:00 PM', start_time, end_time, timezone))
        for event in events:
            service2.events().insert(calendarId='dummytest12313@gmail.com', body=event).execute()
            time.sleep(1)  # Throttle requests to avoid quota limits

    #Weekly Folder
    start_of_week1_str = data[1][0]  # data[1] is the first row, and data[1][0] is the date in that row
    start_of_week1 = datetime.strptime(start_of_week1_str, '%Y-%m-%d')
    weekData = {}  # Stores data for the current week

    for row in data[1:]:  # Skip the header row
        #date, homework, lab = row[0], row[2], row[3]
        date = row[0]
        week_num = get_relative_week_number(start_of_week1, date)
        if week_num not in weekData:
            weekData[week_num] = []
        weekData[week_num].append(row)

        # Process and upload the data for each week
    for week_num, rows in weekData.items():
        currentWeek = f"Week {week_num}"
        process_and_upload_week_data(service, currentWeek, rows)

    # Additional processing for each row
        for row in rows:
            homework, lab = row[2], row[3]
            if homework.strip():  # Check if homework is not empty
                create_and_convert_file(service, homework, week_num, "homework", "solution", currentWeek)
                #create_and_upload_file(service, lab, week_num, "homework_solution_week", currentWeek)
            if lab.strip():  # Check if lab is not empty
                create_and_convert_file(service, lab, week_num, "lab", "report", currentWeek)
                #create_and_upload_file(service, lab, week_num, "lab_template_week", currentWeek)
    weekData.clear()
    if weekData:
        process_and_upload_week_data(service, currentWeek, weekData)
  except HttpError as error:
    print(f"An error occurred: {error}")

#start_of_week1 = datetime(2024, 1, 23)

def get_relative_week_number(start_date, current_date_str):
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
    delta = current_date - start_date
    # Calculate the relative week number, starting from 1
    return delta.days // 7 + 1

def create_and_upload_file(service, content, weekCount, file_prefix, currentWeek):
    """Create and upload a file for homework or lab."""
    file_name = f"{file_prefix}_{weekCount}.txt"
    try:
        with open(file_name, 'w') as file:
            file.write(content)  # Optionally write content to the file

        print(f"File created: {file_name}")
        upload_file_to_drive(service, get_folder_id(currentWeek, service), file_name)
    except Exception as e:
        print(f"Error creating file: {e}")

def create_and_convert_file(service, content, weekCount, file_prefix, file_post, currentWeek):
    """Create and upload a file for homework or lab."""
    #f = open('user.txt', 'r')
    with open('user.txt', 'r') as file:
        f = file.read().rstrip()
    name = f + "_" + file_prefix + "_" + str(weekCount) + "_" + file_post
    file_name = f"{name}.txt"
    # File metadata
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [get_folder_id(currentWeek, service)]
    }
    try:
        with open(file_name, 'w') as file:
            file.write("")  # Optionally write content to the file
        media = MediaFileUpload(file_name, mimetype='text/plain', resumable=True)  # Correct MIME type for upload
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()  # Add convert=True
        print(f"File created: {file_name}")
    except Exception as e:
        print(f"Error creating file: {e}")


def process_and_upload_week_data(service, weekName, weekData):
    # Define your labels here, matching the structure of your Excel data
    labels = ["Date", "Topic", "Assignment", "Lab Due", "Discussion", "Quiz", "Exam"]

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