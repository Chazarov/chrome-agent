from domain.core.container import Container


def main() -> None:
    print("🚀 Тестовый запрос с tool calling к Yandex AI Agent...")

    container = Container()
    response = container.yandex_agent.test()

    print("✓ Ответ модели:")
    print(response)


if __name__ == "__main__":
    main()
