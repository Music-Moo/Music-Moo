# Music-Moo
Gets rid of Spotify by downloading music from Youtube and putting it on Google Drive

> Did you know? [Cows love music](https://www.youtube.com/watch?v=lXKDu6cdXLI)!

![Home Screen](https://imgur.com/N62n54L.gif)

Requires Python 3.6+

1. `pip install -r requirements.txt`
2. Perform Step 1 from [this quickstart](https://developers.google.com/drive/v3/web/quickstart/python) to add API access to Google Drive
2. Perform Step 1 from [this quickstart](https://developers.google.com/youtube/v3/quickstart/python) to add API acces to Youtube
4. Install [ffmpeg](https://ffmpeg.org). You can use a package manager to do that.
5. Run `python moo.py`
6. If this is the first run, a browser will open to grant Music Moo access to your Google Drive and Youtube
7. Go to `localhost:5000` to search Youtube and download songs
8. (Optional) If you have the Youtube links already, make a POST request to `localhost:5000/download` with a JSON in the body of format:
```
{
    "urls": [
        "<youtube_link1>",
        "<youtube_link2>",
        ...
    ]
}
```
9. Download a music player that connects to your Google Drive and play music on your devices
