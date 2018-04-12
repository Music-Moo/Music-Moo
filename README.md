# Music-Moo
Gets rid of Spotify by downloading music from Youtube and putting it on Google Drive

Requires Python 3.6+

1. `pip install -r requirements.txt`
2. Perform Step 1 from [this quickstart](https://developers.google.com/drive/v3/web/quickstart/python)
3. Create a folder in your Google Drive called `Music`
4. Run `python moo.py`
5. Go to `localhost:5000/access` and grant access to your Google Drive
6. Make a POST request to `localhost:5000/` with a JSON in the body of format `{"url": <youtube_url>}`
7. Download a cloud music player to connect to your Google Drive and play music on your devices
