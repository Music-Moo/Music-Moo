# -*- coding: utf-8 -*-

from moo.connection import connect_to_drive, connect_to_youtube

drive_service = connect_to_drive()
youtube_service = connect_to_youtube()


from queue import Queue

download_queue = Queue(100)
convert_queue = Queue(100)
upload_queue = Queue(100)
delete_queue = Queue(200)
done_queue = Queue()


from moo.worker import Worker, download_from_youtube, convert_to_mp3, upload_to_drive, delete_local_file

threads = [
    Worker(download_from_youtube, download_queue, convert_queue),
    Worker(convert_to_mp3, convert_queue, upload_queue),
    Worker(upload_to_drive, upload_queue, delete_queue),
    Worker(delete_local_file, delete_queue, done_queue)
]
for thread in threads:
    thread.start()


from flask import Flask
from moo.views.download import download
from moo.views.gui import gui

app = Flask(__name__)
app.register_blueprint(download)
app.register_blueprint(gui)
