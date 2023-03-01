import os
import json

from googleapiclient.discovery import build

# API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


# class Youtube:
#
#     def __init__(self, api_key: str):
#         self.api_key = api_key


class Channel:

    def __init__(self, channel_id: str):
        self.channel_id = channel_id


    def print_info(self):
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def create_data(self):
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        data = json.dumps(channel, indent=2, ensure_ascii=False)
        return data


# channel_id = 'UC86DMwzxzk1DWqnaAjibUHQ'  # Уральские пельмени
channel_id = 'UCsT0YIqwnpJCM-mx7-gSA4Q'  # TEDx Talks

# 2 экземпляра класса
# ural_pelmeni = Channel('UC86DMwzxzk1DWqnaAjibUHQ')
# ural_pelmeni.print_info()

tedx_talks = Channel('UCsT0YIqwnpJCM-mx7-gSA4Q')
# tedx_talks.print_info()
# print(tedx_talks.create_data())

# Узнаём тип data
print(type(tedx_talks.create_data()))
# Переводим data в формат словаря для создания json
data_dict = json.loads(tedx_talks.create_data())
print(type(data_dict))

# Создаём файл json в проекте, чтобы не загружать каждый раз из YouTube.
with open('youtube_channel.json', 'w') as file:
    json.dump(data_dict, file, indent=2)
