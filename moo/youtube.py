# -*- coding: utf-8 -*-

from moo import youtube_service


def search_youtube(query):
    """
    Performs a search on Youtube for the top videos matching the query string.

    :param str query: Query string to search for
    :return list: List of videos of format {'title': str, 'url': str}
    """

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

    return videos
