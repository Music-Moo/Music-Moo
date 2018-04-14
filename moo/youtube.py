# -*- coding: utf-8 -*-

from moo import m2s


def search_youtube(query):
    """
    Performs a search on Youtube for the top videos matching the query string.

    :param str query: Query string to search for
    :return tuple: (List of videos of format {'title': str, 'id': str}, List of playlists of format {'title': str, 'id': str})
    """

    search_response = m2s.youtube_service.search().list(
        q=query,
        part='id,snippet',
        maxResults=50,
        type='video,playlist'
    ).execute()

    videos = []
    playlists = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == "youtube#video":
            videos.append({
                'title': search_result['snippet']['title'],
                'id': search_result['id']['videoId']
            })
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append({
                'title': search_result['snippet']['title'],
                'id': search_result['id']['playlistId']
            })

    return videos, playlists


def get_playlist_videos(playlist_id):
    """
    Returns a list of videos inside the playlist with the given playlist_id.

    :param str playlist_id: ID of the playlist
    :return tuple: (Playlist title, List of videos of format {'title': str, 'id': str})
    """

    playlist_response = m2s.youtube_service.playlistItems().list(
        playlistId=playlist_id,
        part='id,snippet,contentDetails',
        maxResults=50
    ).execute()

    videos = []

    for search_result in playlist_response.get('items', []):
        videos.append({
            'title': search_result['snippet']['title'],
            'id': search_result['contentDetails']['videoId']
        })

    playlist = m2s.youtube_service.playlists().list(
        part='snippet',
        id=playlist_id
    ).execute()['items'][0]

    return playlist['snippet']['title'], videos
