import os
import pickle
import datetime
import requests
from urllib.error import HTTPError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import numpy as np
import backoff
import time
import pandas as pd

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
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, SCOPES)
    service = build("drive", "v3", credentials=creds)
    # Replace FOLDER_ID with the ID of the folder you want to upload the file to
    folder_id = create_folder(service, "IT212-New") #get_folder_id("IT212", service)
    share_folder_with_email(service, folder_id, "dummytest12313@gmail.com", "writer")

# Create a MediaFileUpload object for the downloaded file
    media = MediaFileUpload('C:/Users/mahya/Downloads/syllabus-generated.docx')

# Set the file metadata
    file_metadata = {
        'name': 'syllabus-generated.docx',
        'parents': [folder_id]
    }
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Load the Excel file
    df = pd.read_excel('C:/Users/mahya/Downloads/schedule.xlsx')

    # Save as a CSV (temporary step)
    df.to_csv('temp.csv', index=False)

    # File metadata
    file_metadata = {
        'name': 'schedule',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [folder_id]
    }

# Media content
    media = MediaFileUpload('temp.csv', mimetype='text/csv', resumable=True)

# Upload file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  except HttpError as error:
    print(f"An error occurred: {error}")

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
    
def share_folder_with_email(service, folder_id, email_address, role='reader'):
    """
    Share a Google Drive folder with a specified email address.

    Args:
    service: Authorized Google Drive service instance.
    folder_id: The ID of the folder to share.
    email_address: The email address to share the folder with.
    role: The role to assign ('reader', 'writer', etc.). Defaults to 'reader'.

    Returns:
    None
    """
    permission = {
        'type': 'user',
        'role': role,
        'emailAddress': email_address
    }

    try:
        service.permissions().create(
            fileId=folder_id,
            body=permission,
            sendNotificationEmail=True,  # Set to False if you don't want to send an email notification
            fields='id'
        ).execute()
        print(f"Folder shared with {email_address} as a {role}.")
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == "__main__":
    main()