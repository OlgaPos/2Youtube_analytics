import datetime
import json
import os

import isodate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Youtube:
    # API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, api_key: str):
        self.api_key = api_key


class Channel:

    def __init__(self, channel_id: str):
        """Экземпляр класса инициализируется по id канала.
        Во время создания экземпляра инициализируются дополнительные атрибуты."""
        self.__channel_id = channel_id

        channel = Youtube.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        data = json.dumps(channel, indent=2, ensure_ascii=False)
        self.info = json.loads(data)
        self.title = self.info['items'][0]['snippet']['title']  # название канала

        self.description = self.info['items'][0]['snippet']['description']  # описание канала
        self.url = 'https://www.youtube.com/channel/' + self.info['items'][0]['id']  # ссылка на канал
        self.subscriber_count = int(self.info['items'][0]["statistics"]["subscriberCount"])  # количество подписчиков
        self.video_count = int(self.info['items'][0]["statistics"]["videoCount"])  # количество видео
        self.view_count = self.info['items'][0]["statistics"]["viewCount"]  # количество просмотров

    @property
    def channel_id(self) -> str:
        """Декоратор позволяет вносить изменения в private атрибут"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API YouTube"""
        return Youtube.youtube

    def to_json(self, path):
        """Сохраняем файл json в проекте, чтобы не загружать каждый раз из YouTube"""
        with open(path, 'w', encoding="UTF-8") as file:
            json.dump(self.info, file, indent=2)

    def __str__(self):
        """Выводим название Youtube-канала пользователю"""
        print(f"Youtube-канал: {self.title}")

    def __gt__(self, other):
        """Сравниваем больше ли у первого Youtube-канала подписчиков, чем у другого"""
        if isinstance(other, Channel):
            return self.subscriber_count > other.subscriber_count
        else:
            raise ValueError("Неправильный формат")

    def __lt__(self, other):
        """Сравниваем меньше ли у первого Youtube-канала подписчиков, чем у другого"""
        if isinstance(other, Channel):
            return self.subscriber_count < other.subscriber_count
        else:
            raise ValueError("Неправильный формат")

    def __add__(self, other):
        """Складываем подписчиков первого Youtube-канала и другого"""
        if isinstance(other, Channel):
            return self.subscriber_count + other.subscriber_count
        else:
            raise ValueError("Неправильный формат")

    def print_info(self):
        channel = Youtube.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    # def create_data(self):
    #     channel = Youtube.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    #     data = json.dumps(channel, indent=2, ensure_ascii=False)
    #     return data


class Video:
    def __init__(self, video_id: str) -> None:
        """ Экземпляр класса инициализируется по id видео.
        Во время создания экземпляра инициализируются дополнительные атрибуты."""
        self.video_id = video_id
        try:
            video = Youtube.youtube.videos().list(id=video_id, part='snippet, statistics').execute()
            data_video = json.dumps(video, indent=2, ensure_ascii=False)
            self.info = json.loads(data_video)
            self.title = self.info['items'][0]['snippet']['title']  # название видео

            self.description = self.info['items'][0]['snippet']['description']  # описание видео
            self.view_count = self.info['items'][0]["statistics"]["viewCount"]  # количество просмотров
            self.like_count = self.info['items'][0]["statistics"]["likeCount"]  # количество лайков
        except IndexError:
            self.info = None
            self.title = None
            self.description = None
            self.view_count = None
            self.like_count = None
        # finally:
        #     print("ended")

    def print_info(self, video_id):
        video = Youtube.youtube.videos().list(id=video_id, part='snippet, statistics').execute()
        print(json.dumps(video, indent=2, ensure_ascii=False))

    def create_data(self, video_id):
        video = Youtube.youtube.videos().list(id=video_id, part='snippet, statistics').execute()
        data = json.dumps(video, indent=2, ensure_ascii=False)
        return data

    def __str__(self) -> str:
        """Выводим название Youtube-канала пользователю"""
        return f"Видео: {self.title}"


class PLVideo(Video):
    def __init__(self, video_id: str, pl_id: str) -> None:
        """Инициализируем клас плейлиста. Наследуем класс Video"""
        super().__init__(video_id)
        self.pl_id = pl_id

        playlist = Youtube.youtube.playlists().list(id=pl_id, part='snippet, contentDetails, status').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']  # название плейлиста

        self.view_count = self.info['items'][0]["statistics"]["viewCount"]  # количество просмотров
        self.like_count = self.info['items'][0]["statistics"]["likeCount"]  # количество лайков

    def __str__(self) -> str:
        """Выводим название видео и название плейлиста пользователю"""
        return f"Видео: {self.title} ({self.playlist_name})"


class PlayList():
    def __init__(self, pl_id: str) -> None:
        """Инициализируем класс плейлиста"""
        self.pl_id = pl_id

        pl = Youtube.youtube.playlists().list(id=self.pl_id, part='snippet, contentDetails').execute()
        self.title = pl['items'][0]['snippet']['title']  # название плейлиста
        self.url = f"https://www.youtube.com/playlist?list={pl_id}"  # url плейлиста

        self.playlist_videos = Youtube.youtube.playlistItems().list(playlistId=pl_id, part='contentDetails',
                                                                    maxResults=52, ).execute()
        data = json.dumps(self.playlist_videos, indent=2, ensure_ascii=False)
        self.info = json.loads(data)

        # Получаем все id видео из плейлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # Получаем все данные о видео из плейлиста
        self.video_response = Youtube.youtube.videos().list(part='contentDetails,statistics',
                                                            id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """Суммируем длину всех видео плейлиста"""
        response = Youtube.youtube.videos().list(part='contentDetails,statistics,snippet',
                                                 id=','.join(self.video_ids)).execute()
        total_duration = datetime.timedelta()
        for video in response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Печатает ссылку на самое популярное видео плейлиста (по количеству лайков)"""
        id_best_video = None
        count_likes = 0
        for video_id in self.video_ids:
            video_info = Channel.get_service().videos().list(part='snippet,statistics', id=video_id).execute()
            iter_count = int(video_info['items'][0]['statistics']['likeCount'])
            if iter_count > count_likes:
                count_likes = iter_count
                id_best_video = video_id
        print(f"https://www.youtube.com/watch?v={id_best_video}")

    def to_json(self, path):
        """Сохраняем файл json в проекте, чтобы не загружать каждый раз из YouTube"""
        with open(path, 'w', encoding="UTF-8") as file:
            json.dump(self.info, file, indent=2)


# print("hw13-01")
# channel_id = 'UC86DMwzxzk1DWqnaAjibUHQ'  # Уральские пельмени
# channel_id = 'UCsT0YIqwnpJCM-mx7-gSA4Q'  # TEDx Talks
#
# tedx_talks = Channel('UCsT0YIqwnpJCM-mx7-gSA4Q')
# tedx_talks.print_info()
# print(tedx_talks.create_data())
#
# # print(type(tedx_talks.create_data()))  # Узнаём тип data
# # data_dict = json.loads(tedx_talks.create_data())  # Переводим data в формат словаря для создания json
# # print(type(data_dict))
#
# ural_pelmeni = Channel('UC86DMwzxzk1DWqnaAjibUHQ')   # экземпляр класса
# ural_pelmeni.print_info()   # выводим информацию про канал

# print("hw13-02")
# print(ural_pelmeni.title)   # получаем значения атрибутов
# print(ural_pelmeni.video_count)
# print(ural_pelmeni.url)
# ural_pelmeni.channel_id = 'Новое название'   # менять не можем
# print(Channel.get_service())   # получаем объект для работы с API вне класса
# ural_pelmeni.to_json('ural_pelmeni.json')   # создаём файл 'ural_pelmeni.json' с данными по каналу

# print("hw14-01")
# ch1 = Channel('UCsT0YIqwnpJCM-mx7-gSA4Q')
# ch2 = Channel('UC86DMwzxzk1DWqnaAjibUHQ')

# print(ch1)
# print(ch2)

# ch1 > ch2
# ch1 < ch2
# ch1 + ch2

# print("hw15-01")
# video1 = Video('9lO06Zxhu88')
# print(video1)
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# print(video2)


# print("hw15-02")
# pl = PlayList('PLdBJapCk3hEFq3f4IiMRtEnCTAAkO2xOh')
# print(pl.title)
# print(pl.url)

# pl.to_json('ural_pelmeni_plist.json')  # создаём файл 'ural_pelmeni_plist.json' с данными по плейлисту

# duration = pl.total_duration
# print(duration)
# print(type(duration))
# print(duration.total_seconds())
#
# pl.show_best_video()


broken_video = Video('9lO06Zxhu8')
print(broken_video.title)
# None
print(broken_video.like_count)
# None
