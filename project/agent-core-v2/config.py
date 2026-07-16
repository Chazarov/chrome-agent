import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self) -> None:
        api_key = os.getenv("YANDEX_CLOUD_API_KEY")
        folder = os.getenv("YANDEX_CLOUD_FOLDER")
        if not api_key or not folder:
            message = (
                "❌ Укажите YANDEX_CLOUD_API_KEY и YANDEX_CLOUD_FOLDER "
                "в переменных окружения"
            )
            print(message)
            raise ValueError(message)

        self.YANDEX_CLOUD_API_KEY: str = api_key
        self.YANDEX_CLOUD_FOLDER: str = folder
        self.YANDEX_AI_URL: str = "https://ai.api.cloud.yandex.net/v1"
        self.YANDEX_CLOUD_MODEL: str = "yandexgpt-5.1/latest"


config = Config()
