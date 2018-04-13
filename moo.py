# -*- coding: utf-8 -*-

from flask import Flask, request, render_template

from worker import download_queue, youtube_service

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form['searchbar-input']
    search_response = youtube_service.search().list(
        q=query,
        part="id,snippet",
        maxResults=50
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append({
                'title': search_result['snippet']['title'],
                'url': 'http://www.youtube.com/watch?v=' + search_result['id']['videoId']
            })

    return render_template('results.html', videos=videos)


@app.route('/download', methods=['POST'])
def download():
    urls = request.get_json().get('urls')
    for url in urls:
        download_queue.put(url)
    return 'Download request processed!', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
