import datetime, json, os, isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        self.id_video = id_video
        self.playlist = self.youtube.playlists().list(part='snippet',
                                                      id=id_video).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={id_video}"
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=self.id_video,
            part='contentDetails',
            maxResults=50,
        ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in
                          self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.video_ids)
        ).execute()
        self.video_response_info = json.dumps(self.video_response, indent=2)

    def sum_timedelta(self, lst: list) -> datetime.timedelta:
        """
        Вспомогательный метод для сложения всех временных отрезков роликов
        """
        summ = datetime.timedelta()
        for item in lst:
            summ += item
        return summ

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        return self.sum_timedelta(
            [isodate.parse_duration(video['contentDetails']['duration']) for
             video in self.video_response['items']])

    def show_best_video(self) -> str:
        """
        Находит самое популярное видео по количеству лайков
         и возвращает ссылку на него
        """
        max_like_count = 0
        max_video_id = \
            max([(video["statistics"]["likeCount"], video['id']) for video in
                 self.video_response['items']], key=lambda x: int(x[0]))[1]
        return f'https://youtu.be/{max_video_id}'
