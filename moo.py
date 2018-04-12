
from queue import Queue

from apiclient.discovery import build
from flask import Flask, request
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from pytube import YouTube
from oauth2client import file, client, tools

from worker import Worker

app = Flask(__name__)


def connect_to_drive():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def download_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    print(f"Download for {stream.default_filename} has started")
    stream.download()
    print(f"Download for {stream.default_filename} is complete")

    return stream.default_filename


def upload_to_drive(file_name):
    response = drive_service.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder'").execute()
    folder_id = response.get('files', [])[0]['id']
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    print(f"Upload for {file_name} has started")
    media = MediaFileUpload(file_name, mimetype='audio/mpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Upload for {file_name} is complete, id is {file.get('id')}")

    return file.get('id')

drive_service = connect_to_drive()

download_queue = Queue(100)
upload_queue = Queue(100)
done_queue = Queue()

threads = [
    Worker(download_from_youtube, download_queue, upload_queue),
    Worker(upload_to_drive, upload_queue, done_queue)
]
for thread in threads:
    thread.start()


@app.route('/', methods=['POST'])
def index():
    url = request.json.get('url')
    download_queue.put(url)
    return 'Download request processed!', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
