# -*- coding: utf-8 -*-
from time import time
from isodate import parse_duration

from moo import m2s


def search_youtube(query, short=False):
    """
    Performs a search on Youtube for the top videos matching the query string.

    :param str query: Query string to search for
    :param boolean short: If this is set to True, it will only search for videos <20 minutes long
    :return tuple: (List of videos of format {'title': str, 'duration': str, 'id': str}, List of playlists of format {'title': str, 'id': str})
    """
    
    items = []

    if short:
        kwargs = {'type': 'video', 'maxResults': 30, 'videoDuration': 'short'}
        search_response = m2s.youtube_service.search().list(
            q=query,
            part='id,snippet',
            **kwargs
        ).execute()
        items += search_response.get('items', [])
        kwargs = {'type': 'video', 'maxResults': 20, 'videoDuration': 'medium'}
    else:
        kwargs = {'type': 'video,playlist', 'maxResults': 50}

    search_response = m2s.youtube_service.search().list(
        q=query,
        part='id,snippet',
        **kwargs
    ).execute()
    items += search_response.get('items', [])

    video_ids = []
    videos = []
    playlists = []
    
    for search_result in search_response.get('items', []):
        if search_result['snippet']['liveBroadcastContent'] == 'none':
            if search_result['id']['kind'] == "youtube#video":
                video_ids.append(search_result['id']['videoId'])
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append({
                    'title': search_result['snippet']['title'],
                    'id': search_result['id']['playlistId']
                })
    
    video_response = m2s.youtube_service.videos().list(
        id=','.join(video_ids),
        part='id,snippet,contentDetails'
    ).execute()
    
    for video in video_response.get('items', []):
        videos.append({
                    'title': video['snippet']['title'],
                    'duration': str(parse_duration(video['contentDetails']['duration'])),
                    'id': video['id']
                })

    return videos, playlists


def get_playlist_videos(playlist_id):
    """
    Returns a list of videos inside the playlist with the given playlist_id.

    :param str playlist_id: ID of the playlist
    :return tuple: (Playlist title, List of videos of format {'title': str, 'duration': str, 'id': str})
    """

    playlist_response = m2s.youtube_service.playlistItems().list(
        playlistId=playlist_id,
        part='id,snippet,contentDetails',
        maxResults=50
    ).execute()

    video_ids = []
    videos = []

    for search_result in playlist_response.get('items', []):
        video_ids.append(search_result['contentDetails']['videoId'])

    video_response = m2s.youtube_service.videos().list(
        id=','.join(video_ids),
        part='id,snippet,contentDetails'
    ).execute()

    for video in video_response.get('items', []):
        videos.append({
                    'title': video['snippet']['title'],
                    'duration': str(parse_duration(video['contentDetails']['duration'])),
                    'id': video['id']
                })

    playlist = m2s.youtube_service.playlists().list(
        part='snippet',
        id=playlist_id
    ).execute()['items'][0]

    return playlist['snippet']['title'], videos
