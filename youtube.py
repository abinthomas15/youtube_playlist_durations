# This script will check the total duration of any youtube playlist

import re
from datetime import timedelta
from googleapiclient.discovery import build

playlist_id = 'PLLa_h7BriLH0FzTY5aBFpH-vciOiEf4Br'

api_key = "AIzaSyAZ-K94k0MAp3A8sqFMvdZP4mkRJ7eNKaQ"

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id
                    ,maxResults=50,pageToken=nextPageToken)

    pl_response = pl_request.execute()

    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(part='contentDetails',id=','.join(vid_ids))

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        if hours is not None:
            hours = int(hours.group(1))
        else:
            hours = 0
        if minutes is not None:
            minutes = int(minutes.group(1))
        else:
            minutes = 0
        if seconds is not None:
            seconds = int(seconds.group(1))
        else:
            seconds = 0

        videos_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        total_seconds += videos_seconds
    
    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds,60)
hours, minutes = divmod(minutes,60)

print(f"{hours}:{minutes}:{seconds}")
