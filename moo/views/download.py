# -*- coding: utf-8 -*-

from flask import Blueprint, request

from moo import download_queue

download = Blueprint('download', __name__)


@download.route('/download', methods=['POST'])
def add_to_download_queue():
    urls = request.get_json().get('urls')
    for url in urls:
        download_queue.put(url)
    return 'Download request processed!', 200
