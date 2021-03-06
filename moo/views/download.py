# -*- coding: utf-8 -*-

from flask import Blueprint, request

from moo import m2s
from moo.helpers import get_urls_from_videos
from moo.youtube import get_playlist_videos

download = Blueprint('download', __name__)


@download.route('/download', methods=['POST'])
def add_to_download_queue():
    urls = request.get_json().get('urls')
    for url in urls:
        m2s.add_to_queue(url)
    return 'Download request processed!', 200


@download.route('/download/<playlist_id>')
def add_playlist_to_download_queue(playlist_id):
    _, videos = get_playlist_videos(playlist_id)
    urls = get_urls_from_videos(videos)
    for url in urls:
        m2s.add_to_queue(url)
    return 'Download request processed!', 200
