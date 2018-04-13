# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template

from moo.youtube import search_youtube

gui = Blueprint('gui', __name__)


@gui.route('/')
def index():
    return render_template('index.html')


@gui.route('/search', methods=['POST'])
def search():
    query = request.form['searchbar-input']
    videos = search_youtube(query)
    return render_template('results.html', videos=videos)
