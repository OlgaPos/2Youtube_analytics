import os
import json
from googleapiclient.discovery import build


class Youtube:

    # API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, api_key: str):
        self.api_key = api_key


class Channel:

    def __init__(self, channel_id: str):
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

    # def print_info(self):
    #     channel = Youtube.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    #     print(json.dumps(channel, indent=2, ensure_ascii=False))

    # def create_data(self):
    #     channel = Youtube.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    #     data = json.dumps(channel, indent=2, ensure_ascii=False)
    #     return data


# channel_id = 'UC86DMwzxzk1DWqnaAjibUHQ'  # Уральские пельмени
# channel_id = 'UCsT0YIqwnpJCM-mx7-gSA4Q'  # TEDx Talks
#
# # 2 экземпляра класса
# # ural_pelmeni = Channel('UC86DMwzxzk1DWqnaAjibUHQ')
# # ural_pelmeni.print_info()
#
# tedx_talks = Channel('UCsT0YIqwnpJCM-mx7-gSA4Q')
# # tedx_talks.print_info()
# # print(tedx_talks.create_data())
#
# # print(type(tedx_talks.create_data()))  # Узнаём тип data
# # data_dict = json.loads(tedx_talks.create_data())  # Переводим data в формат словаря для создания json
# # print(type(data_dict))
# #
#
#
# # получаем значения атрибутов
# print(tedx_talks.title)
# print(tedx_talks.video_count)
# print(tedx_talks.url)
#
# # менять не можем
# tedx_talks.channel_id = 'Новое название'
#
# # можем получить объект для работы с API вне класса
# print(Channel.get_service())
#
# # создать файл 'tedx_talks.json' в данными по каналу
# tedx_talks.to_json('tedx_talks.json')

ch1 = Channel('UCsT0YIqwnpJCM-mx7-gSA4Q')
ch2 = Channel('UC86DMwzxzk1DWqnaAjibUHQ')

print(ch1)
print(ch2)

ch1 > ch2

ch1 < ch2

ch1 + ch2
