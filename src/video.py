import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_info = self.youtube.videos().list(id=self.video_id,
                                                     part='snippet,statistics').execute()
        self.title = self.video_info['items'][0]['snippet']['title']
        self.url = 'https://youtu.be/' + self.video_id
        self.views = self.video_info['items'][0]['statistics']['viewCount']
        self.likes = self.video_info['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id, playlist_id):
        self.playlist_id = playlist_id
        super().__init__(video_id=id)
