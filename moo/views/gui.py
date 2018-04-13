# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template

from moo.youtube import search_youtube, get_playlist_videos

gui = Blueprint('gui', __name__)


@gui.route('/')
def index():
    return render_template('index.html')


@gui.route('/search', methods=['POST'])
def search():
    query = request.form['searchbar-input']
    videos, playlists = search_youtube(query)
    return render_template('results.html', videos=videos, playlists=playlists)


@gui.route('/playlist/<playlist_id>')
def playlist(playlist_id):
    playlist_title, videos = get_playlist_videos(playlist_id)
    return render_template('playlist.html', playlist_title=playlist_title, videos=videos)
