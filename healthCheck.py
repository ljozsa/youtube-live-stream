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

youtube = get_authenticated_service()
list_streams_request = youtube.liveStreams().list(
part="id,snippet,cdn,status",
mine=True,
maxResults=50
).execute()
import os
import time

for item in list_streams_request.get("items", []):
  print item['snippet']['title'] + " stream status " + item['status']['streamStatus'] + " health status "+ item['status']['healthStatus']['status']

#print "-----------------------------"
#
#list_streams_request = youtube.liveBroadcasts().list(
#part="id,snippet,contentDetails,status",
#mine=True,
#maxResults=1
#).execute()
#
#broadcasts = []
#list_broadcasts_response = youtube.liveBroadcasts().list(
#    broadcastStatus="upcoming",
#    part="id,snippet,contentDetails",
#    maxResults=50
#  ).execute()
#
#broadcasts = list_broadcasts_response['items']
#
#print list_broadcasts_response
#for item in list_broadcasts_response:
#  print '+-+'
#  print item
#  print '-+-'
#
#while 'nextPageToken' in list_broadcasts_response:
#  pt = list_broadcasts_response['nextPageToken']
#  list_broadcasts_response = youtube.liveBroadcasts().list(
#      broadcastStatus="all",
#      part="id,snippet,contentDetails",
#      maxResults=50,
#      pageToken=pt
#    ).execute()
#  broadcasts+=list_broadcasts_response['items']
#
#print broadcasts
#print '++++++++++++++++++++++++++'
#for item in broadcasts:
#  print '+-+'
#  print item['snippet']['scheduledStartTime']
#  print '-+-'
#  
#  print item['snippet']['scheduledStartTime']
#print list_streams_request
