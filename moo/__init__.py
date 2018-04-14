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


from flask import Flask
from moo.views.download import download
from moo.views.gui import gui

app = Flask(__name__)
app.register_blueprint(download)
app.register_blueprint(gui)
