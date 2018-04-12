
from pytube import YouTube
from googleapiclient.http import MediaFileUpload
from oauth2client import file, client, tools
from httplib2 import Http
from apiclient.discovery import build


def download(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()
    return stream.default_filename


def connect_to_drive():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def upload_to_drive(drive_service, file_name):
    response = drive_service.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder'").execute()

    folder_id = response.get('files', [])[0]['id']

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_name, mimetype='audio/mpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Upload complete, id is {file.get('id')}")

service = connect_to_drive()
file_name = download('https://www.youtube.com/watch?v=DhHGDOgjie4')
upload_to_drive(service, file_name)
