import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    def __init__(self):
        if not self.YANDEX_CLOUD_API_KEY or not self.YANDEX_CLOUD_FOLDER:
            print("❌ Укажите YANDEX_CLOUD_API_KEY и YANDEX_CLOUD_FOLDER в переменных окружения")
            raise ValueError("❌ Укажите YANDEX_CLOUD_API_KEY и YANDEX_CLOUD_FOLDER в переменных окружения")


    YANDEX_CLOUD_API_KEY=os.getenv("YANDEX_CLOUD_API_KEY")
    YANDEX_CLOUD_FOLDER=os.getenv("YANDEX_CLOUD_FOLDER")
    YANDEX_AI_URL="https://ai.api.cloud.yandex.net/v1"
    YANDEX_CLOUD_MODEL = "yandexgpt-5.1/latest"



config = Config()

