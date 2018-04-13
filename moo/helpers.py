# -*- coding: utf-8 -*-

def get_urls_from_videos(videos):
    """
    Converts a list of videos (format that is passed to the templates) to a list of video URLs to pass to the downloader.

    :param list videos: List of videos of format {'title': str, 'id': str}
    :return list: List of videos URLs
    """

    return ['http://www.youtube.com/watch?v=' + video['id'] for video in videos]
