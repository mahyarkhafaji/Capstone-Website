from Google import Create_Service
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import numpy as np

def main():
    CLIENT_SECRET_FILE = 'client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    folder_id = '13julqBiMDaTy6GC7f_V2YYfc1EO-9PQl'

    #Authorize the API
    scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']
    file_name = 'client_service.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = gspread.authorize(creds)

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