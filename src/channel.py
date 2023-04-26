import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=self.__channel_id,
                                                         part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet'][
            'description']
        self.url = f'https://www.youtube.com/channel/{self.channel_info["items"][0]["id"]}'
        self.subs = self.channel_info['items'][0]['statistics'][
            'subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics'][
            'videoCount']
        self.views = self.channel_info['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id,
                                               part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, f):
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subs,
            "video_count": self.video_count,
            "view_count": self.views
        }
        with open(f, mode="w", encoding="utf-8") as out_f:
            json.dump(data, out_f, indent=4)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subs) + int(other.subs)

    def __radd__(self, other):
        return int(self.subs) + int(other.subs)

    def __sub__(self, other):
        return int(self.subs) - int(other.subs)

    def __rsub__(self, other):
        return int(self.subs) - int(other.subs)

    def __lt__(self, other):
        return int(self.subs) < int(other.subs)

    def __le__(self, other):
        return int(self.subs) <= int(other.subs)

    def __eq__(self, other):
        return int(self.subs) == int(other.subs)

    def __ne__(self, other):
        return int(self.subs) != int(other.subs)

    def __gt__(self, other):
        return int(self.subs) > int(other.subs)

    def __ge__(self, other):
        return int(self.subs) >= int(other.subs)
