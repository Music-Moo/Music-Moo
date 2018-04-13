# -*- coding: utf-8 -*-

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def connect_to_drive():
    """
    Creates connection to the Google Drive API and returns the service object to make requests.

    :return googleapiclient.discovery.Resource:
    """

    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('drive_credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def connect_to_youtube():
    """
    Creates connection to the Youtube API and returns the service object to make requests.

    :return googleapiclient.discovery.Resource:
    """

    SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
    store = file.Storage('youtube_credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('youtube', 'v3', http=creds.authorize(Http()))
    return service  
