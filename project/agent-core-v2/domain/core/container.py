from config import config
from infrastructure.ports.yandex_cloude.agent.api import YandexAgentConnector


class Container:
    def __init__(self) -> None:
        self.yandex_agent = YandexAgentConnector(
            api_key=config.YANDEX_CLOUD_API_KEY,
            url=config.YANDEX_AI_URL,
            yandex_cloude_folder=config.YANDEX_CLOUD_FOLDER,
            model=config.YANDEX_CLOUD_MODEL,
        )
