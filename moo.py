
import os
from queue import Queue
import subprocess
from time import time

from apiclient.discovery import build
from ffmpy import FFmpeg
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
    stream = yt.streams.first()
    print(f"Download for {stream.default_filename} has started")
    start_time = time()
    stream.download()
    end_time = time()
    print(f"Download for {stream.default_filename} has finished in {end_time - start_time} seconds")

    return stream.default_filename


def convert_to_mp3(file_name):
    new_file_name = os.path.splitext(file_name)[0] + '.mp3'
    ff = FFmpeg(
        inputs={file_name: None},
        outputs={new_file_name: None}
    )
    print(f"Conversion for {file_name} has started")
    start_time = time()
    ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time()
    print(f"Conversion for {file_name} has finished in {end_time - start_time} seconds")

    delete_queue.put(file_name)
    return new_file_name


def upload_to_drive(file_name):
    response = drive_service.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder'").execute()
    folder_id = response.get('files', [])[0]['id']
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    print(f"Upload for {file_name} has started")
    start_time = time()
    media = MediaFileUpload(file_name, mimetype='audio/mpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    end_time = time()
    print(f"Upload for {file_name} has finished in {end_time - start_time} seconds, id is {file.get('id')}")

    return file_name


def delete_local_file(file_name):
    try:
        os.remove(file_name)
        print(f"Deletion for {file_name} has finished")
        return file_name
    except OSError:
        pass

drive_service = connect_to_drive()

download_queue = Queue(100)
convert_queue = Queue(100)
upload_queue = Queue(100)
delete_queue = Queue(200)
done_queue = Queue()

threads = [
    Worker(download_from_youtube, download_queue, convert_queue),
    Worker(convert_to_mp3, convert_queue, upload_queue),
    Worker(upload_to_drive, upload_queue, delete_queue),
    Worker(delete_local_file, delete_queue, done_queue)
]
for thread in threads:
    thread.start()


@app.route('/', methods=['POST'])
def index():
    urls = request.json.get('urls')
    for url in urls:
        download_queue.put(url)
    return 'Download request processed!', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
