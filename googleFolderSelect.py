from os.path import dirname, join
import os
import pickle
import datetime
from collections import namedtuple
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import numpy as np

def Create_Service(client_secret_file, api_name, api_version, *scopes, prefix=''):
	CLIENT_SECRET_FILE = client_secret_file
	API_SERVICE_NAME = api_name
	API_VERSION = api_version
	SCOPES = [scope for scope in scopes[0]]
	
	cred = None
	working_dir = os.environ["HOME"]
	token_dir = 'token files'
	pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

	### Check if token dir exists first, if not, create the folder
	if not os.path.exists(join(working_dir, token_dir)):
		os.mkdir(join(working_dir, token_dir))

	if os.path.exists(join(working_dir, token_dir, pickle_file)):
		with open(join(working_dir, token_dir, pickle_file), 'rb') as token:
			cred = pickle.load(token)

	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
			cred = flow.run_local_server()

		with open(join(working_dir, token_dir, pickle_file), 'wb') as token:
			pickle.dump(cred, token)

	try:
		service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
		print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
		return service
	except Exception as e:
		print(e)
		print(f'Failed to create service instance for {API_SERVICE_NAME}')
		os.remove(join(working_dir, token_dir, pickle_file))
		return None
	
def main():
    #Authorize the API
    scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']
    file_name = '/data/user/0/com.example.myloginapp/files/client_service.json'
        
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = gspread.authorize(creds)

    CLIENT_SECRET_FILE = '/data/user/0/com.example.myloginapp/files/client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    folder_id = '13julqBiMDaTy6GC7f_V2YYfc1EO-9PQl'

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    #Fetch the sheet
    worksheet = client.open('IT212_Schedule').sheet1

    def get_id(fname):
        query = f"parents = '{folder_id}'"
        response = service.files().list(q=query, fields= 'files(id,name)').execute()
        files = response.get('files')
        if files:
            google_file_name=  files[0].get(fname)
            google_file_id = files[0].get('id')
        else:
            print("File Not Found")
        return google_file_id

    def create_folder(fname):

        file_metadata = {
            'name': fname,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id],
        }
        service.files().create(body=file_metadata).execute()

    r = 0               # Keeps track of rows
    weekCount = 1       # Keeps track of weeks
    lab = 1             # Keeps track of labs
    hw = 1              # Keeps track of homeworks
    lec = 1             # Keeps track of lectures
    w = 2               # Keep track of biweekly count
    rowRange = len(worksheet.get_all_values()) # Number of rows
    remainder = (rowRange - 1) % 2

    maxRow = (((rowRange - 1) // 2) + remainder)

    array = np.array(worksheet.get_all_values())

    arr = []

    for x in array:
        for y in x:
            arr.append(y)

    def remove():
        for element in range(9):
            arr.pop(0)

    remove()

    # Parse through worksheet to manipulate cells
    for row in range(maxRow):

        # Create folder for each week of classes with its necessary contents

        if r < rowRange:
            weekPath = 'Week ' + str(weekCount)
            weekCount += 1
            create_folder(weekPath)
            for week in range(2):
                if len(arr) > 0:
                    if len(arr[1]) > 0:
                        file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'reading' + str(lec) +".txt", 'mimeType':'text/csv'})
                        if len(arr[4]) > 0:
                            file1.SetContentString(arr[4] + " ")
                            if len(arr[5]) > 0:
                                file1.SetContentString(arr[4] + " " + arr[5])
                            if len(arr[7]) > 0 :
                                file1.SetContentString(arr[4] + " " + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[5]) > 0:
                                    file1.SetContentString(arr[4] + " " + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value)
                            if len(arr[8]) > 0:
                                file1.SetContentString(arr[4] + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[5]) > 0:
                                    file1.SetContentString(arr[4] + " " + arr[5] + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[7]) > 0:
                                    file1.SetContentString(arr[4] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                    if len(arr[5]) > 0:
                                        file1.SetContentString(arr[4] + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                        file1.Upload()
                        lec += 1
                        if len(arr[2]) > 0:
                            file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'Lab' + str(lab) +".docx", 'mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
                            lab +=1
                            file1.Upload()
                        if len(arr[6]) > 0:
                            file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'HW' + str(hw) +".docx", 'mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
                            hw += 1
                            file1.Upload()
                    elif len(arr[1]) == 0:
                        file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'reading' + str(lec) +".txt", 'mimeType':'text/csv'})
                        if len(arr[4]) > 0:
                            file1.SetContentString(arr[4] + " ")
                            if len(arr[5]) > 0:
                                file1.SetContentString(arr[4] + " " + arr[5])
                            if len(arr[7]) > 0 :
                                file1.SetContentString(arr[4] + " " + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[5]) > 0:
                                    file1.SetContentString(arr[4] + " " + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value)
                            if len(arr[8]) > 0:
                                file1.SetContentString(arr[4] + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[5]) > 0:
                                    file1.SetContentString(arr[4] + " " + arr[5] + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                if len(arr[7]) > 0:
                                    file1.SetContentString(arr[4] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                                    if len(arr[5]) > 0:
                                        file1.SetContentString(arr[4] + arr[5] + ' HW' + arr[7] + ' is due ' + worksheet.acell('A' + str(w)).value + ' Lab' + arr[8] + ' is due ' + worksheet.acell('A' + str(w)).value)
                        file1.Upload()
                        lec += 1
                        if len(arr[2]) > 0:
                            file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'Lab' + str(lab) +".docx", 'mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
                            lab +=1
                            file1.Upload()
                        if len(arr[6]) > 0:
                            file1 = drive.CreateFile({'parents': [{'id': get_id(weekPath)}],'title': 'HW' + str(hw) +".docx", 'mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
                            hw += 1
                            file1.Upload()
                    w += 1
                    remove()
            r +=2

if __name__ == "__main__":
    main()