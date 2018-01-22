#!/usr/bin/python
# vim: tabstop=4 expandtab shiftwidth=2 softtabstop=2

import httplib2
import os
import sys
import csv
from datetime import datetime
import json
import pytz
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

local = pytz.timezone ("Europe/Prague")
streams = [[],[]]
broadcasts = [[],[]]

def myconverter(o):
    if isinstance(o, datetime):
      return o.strftime("%Y-%m-%dT%H:%M:%S+01:00")

def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, None)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def refresh_streams():
  streams = [[],[]]
  list_streams_request = youtube.liveStreams().list(
  part="id,snippet",
  mine=True,
  maxResults=50
  ).execute()

  for item in list_streams_request.get("items", []):
    streams[0].append(item['snippet']['title'])
    streams[1].append(item['id'])

  return streams

def refresh_broadcasts():
  broadcasts = [[],[]]
  list_broadcasts_response = youtube.liveBroadcasts().list(
    broadcastStatus="all",
    part="id,snippet",
    maxResults=50
  ).execute()

  for broadcast in list_broadcasts_response.get("items", []):
    broadcasts[0].append(broadcast['snippet']['title'])
    broadcasts[1].append(broadcast['id'])

  while 'nextPageToken' in list_broadcasts_response:
    pt = list_broadcasts_response['nextPageToken']
    list_broadcasts_response = youtube.liveBroadcasts().list(
      broadcastStatus="all",
      part="id,snippet",
      maxResults=50,
      pageToken=pt
    ).execute()
    for broadcast in list_broadcasts_response.get("items", []):
      broadcasts[0].append(broadcast['snippet']['title'])
      broadcasts[1].append(broadcast['id'])

  return broadcasts

if __name__ == "__main__":
  youtube = get_authenticated_service()
  streams = refresh_streams()
  broadcasts = refresh_broadcasts()

  schedule = [] 
  filename = "final-sorted.csv"
  with open(filename, 'rb') as csvfile:
    csv_parsed = csv.reader(csvfile, delimiter=',', quotechar='"')
    for record in csv_parsed:
      recording_start_t = json.dumps(datetime.strptime(record[1], "%m/%d/%Y %H:%M:%S"), default = myconverter).strip('"')
      recording_stop_t = json.dumps(datetime.strptime(record[2], "%m/%d/%Y %H:%M:%S"), default = myconverter).strip('"')

      naive = datetime.strptime(record[1], "%m/%d/%Y %H:%M:%S")
      local_dt = local.localize(naive, is_dst=None)
      utc_dt = local_dt.astimezone (pytz.utc)
      title = (record[7].replace(';',',') + ": " + record[5][:126] + '..') if len(record[7].replace(';',',') + ": " +  record[5]) > 126 else record[7].replace(';',',') + ": " +  record[5]

      print title
      try:
        broadcast_key_index = broadcasts[0].index(title)
        broadcast_id = broadcasts[1][broadcast_key_index]
      except ValueError:
        insert_broadcast_response = youtube.liveBroadcasts().insert(
          part="snippet,status",
          body=dict(
            snippet=dict(
              title=title,
              scheduledStartTime=recording_start_t,
              scheduledEndTime=recording_stop_t,
              description=record[6]
            ),
            status=dict(
            privacyStatus="public"
            )
          )
        ).execute()
        broadcast_id = insert_broadcast_response['id']
      else:
        insert_broadcast_response = youtube.liveBroadcasts().update(
          part="id,snippet,status",
          body=dict(
            id=broadcast_id,
            snippet=dict(
              title=title,
              scheduledStartTime=recording_start_t,
              scheduledEndTime=recording_stop_t,
              description=record[6]
            ),
            status=dict(
            privacyStatus="public"
            )
          )
        ).execute()

      print insert_broadcast_response

      response = youtube.videos().update(
        part = 'snippet',
        body = dict(
          id = broadcast_id,
          snippet=dict(
            title = title,
            categoryId=28,
            description=record[6],
            tags = record[-1].split(',')
          )
        )
      ).execute()

      try:
        stream_key_index = streams[0].index(record[8])
        stream_id =  streams[1][stream_key_index]
      except ValueError:
        insert_stream_response = youtube.liveStreams().insert(
          part="snippet,cdn",
          body=dict(
            snippet=dict(
              title=record[8]
            ),
            cdn=dict(
              frameRate="variable",
              resolution="variable",
              ingestionType="rtmp",
              )
            )
          ).execute()
        stream_id = insert_stream_response['id']

      bind_broadcast_response = youtube.liveBroadcasts().bind(
        part="id,contentDetails",
        id=insert_broadcast_response['id'],
        streamId=stream_id
      ).execute()

      broadcasts = refresh_broadcasts()
