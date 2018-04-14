# -*- coding: utf-8 -*-

from music2storage import Music2Storage

m2s = Music2Storage()
m2s.connect_drive()
m2s.connect_youtube()
m2s.start_workers(1)

from flask import Flask
from moo.views.download import download
from moo.views.gui import gui

app = Flask(__name__)
app.register_blueprint(download)
app.register_blueprint(gui)
