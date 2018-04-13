# -*- coding: utf-8 -*-

from queue import Queue
import os
import subprocess
from threading import Thread
from time import time

from apiclient.discovery import build
from ffmpy import FFmpeg
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from pytube import YouTube
from oauth2client import file, client, tools


def connect_to_drive():
    """
    Creates connection to the Google Drive API and returns the service object to make requests.

    :return googleapiclient.discovery.Resource:
    """

    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('drive_credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def connect_to_youtube():
    """
    Creates connection to the Youtube API and returns the service object to make requests.

    :return googleapiclient.discovery.Resource:
    """

    SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
    store = file.Storage('youtube_credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('youtube', 'v3', http=creds.authorize(Http()))
    return service  

drive_service = connect_to_drive()
youtube_service = connect_to_youtube()


class Worker(Thread):
    """Worker that processes items from an input queue and puts the result into an output queue."""

    def __init__(self, func, in_queue, out_queue):
        """
        Builds a worker by taking a function that does work on items from the input queue to be put in the output queue.

        :param function func: Function that does work on items from the input queue
        :param Queue in_queue: Input queue
        :param Queue out_queue: Output queue
        """
        
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        """
        Method that gets run when the Worker thread is started.

        When there's an item in in_queue, it takes it out, passes it to func as an argument, and puts the result in out_queue.
        """

        while True:
            item = self.in_queue.get()
            result = self.func(item)
            self.out_queue.put(result)


def download_from_youtube(url):
    """
    Downloads an MP4 or WebM file that is associated with the video at the URL passed.

    :param str url: URL of the video to be downloaded
    :return str: Filename of the file in local storage
    """

    yt = YouTube(url)
    stream = yt.streams.first()
    print(f"Download for {stream.default_filename} has started")
    start_time = time()
    stream.download()
    end_time = time()
    print(f"Download for {stream.default_filename} has finished in {end_time - start_time} seconds")

    return stream.default_filename


def convert_to_mp3(file_name):
    """
    Converts the file associated with the file_name passed into an MP3 file.

    :param str file_name: Filename of the original file in local storage
    :return str: Filename of the new file in local storage
    """

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
    """
    Uploads the file associated with the file_name passed to Google Drive in the Music folder (creates it in root if it doesn't exist).

    :param str file_name: Filename of the file to be uploaded
    :return str: Original filename passed as an argument (in order for the worker to send it to the delete queue)
    """

    response = drive_service.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false").execute()

    try:
        folder_id = response.get('files', [])[0]['id']
    except IndexError:
        print('Music folder is missing. Creating it.')
        folder_metadata = {
            'name': 'Music',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

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
    """
    Deletes the file associated with the file_name passed from local storage.

    :return str: Filename of the file that was just deleted
    """

    try:
        os.remove(file_name)
        print(f"Deletion for {file_name} has finished")
        return file_name
    except OSError:
        pass

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
