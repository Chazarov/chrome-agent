import json
from typing import Any, Callable

import openai

ToolSpec = dict[str, Any]
ToolHandler = Callable[..., Any]


class YandexAgentConnector:
    def __init__(self, api_key: str, url: str, yandex_cloude_folder: str, model: str) -> None:
        self._api_key = api_key
        self._url = url
        self._project_id = yandex_cloude_folder
        self._model = model
        self._make_client()

    def _make_client(self) -> None:
        self._client = openai.OpenAI(
            api_key=self._api_key,
            base_url=self._url,
            project=self._project_id,
        )

    def _model_uri(self) -> str:
        return f"gpt://{self._project_id}/{self._model}"

    def create_response(
        self,
        input: str | list[Any],
        tools: list[ToolSpec] | None = None,
        instructions: str = "",
        previous_response_id: str | None = None,
        temperature: float = 0.3,
        max_output_tokens: int = 500,
    ) -> Any:
        kwargs: dict[str, Any] = {
            "model": self._model_uri(),
            "temperature": temperature,
            "instructions": instructions,
            "input": input,
            "max_output_tokens": max_output_tokens,
        }

        if tools:
            kwargs["tools"] = tools
        if previous_response_id:
            kwargs["previous_response_id"] = previous_response_id

        return self._client.responses.create(**kwargs)

    @staticmethod
    def get_function_calls(response: Any) -> list[Any]:
        return [
            item
            for item in getattr(response, "output", [])
            if getattr(item, "type", "") == "function_call"
        ]

    def submit_tool_output(
        self,
        previous_response_id: str,
        call_id: str,
        output: str,
        tools: list[ToolSpec],
        instructions: str = "",
    ) -> Any:
        return self.create_response(
            input=[
                {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": output,
                }
            ],
            tools=tools,
            instructions=instructions,
            previous_response_id=previous_response_id,
        )

    def run_with_tools(
        self,
        input_text: str,
        tools: list[ToolSpec],
        handlers: dict[str, ToolHandler],
        instructions: str = "",
    ) -> str:
        response = self.create_response(
            input=input_text,
            tools=tools,
            instructions=instructions,
        )

        calls = self.get_function_calls(response)
        if not calls:
            return str(response.output_text)

        for call in calls:
            handler = handlers.get(call.name)
            if handler is None:
                continue

            args = json.loads(getattr(call, "arguments", "{}") or "{}")
            if not isinstance(args, dict):
                raise TypeError(f"Ожидался dict аргументов для {call.name}, получено {type(args)}")

            result = handler(**args)
            output = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)

            response = self.submit_tool_output(
                previous_response_id=response.id,
                call_id=call.call_id,
                output=output,
                tools=tools,
                instructions=instructions,
            )

        return str(response.output_text)

    def test(self) -> str:
        tools: list[ToolSpec] = [
            {
                "type": "function",
                "name": "get_weather",
                "description": "Получить текущую погоду для указанного города.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Название города, например: Москва или Санкт-Петербург",
                        },
                    },
                    "required": ["city"],
                },
            }
        ]

        def get_weather(city: str) -> dict[str, str]:
            return {
                "город": city,
                "температура": "12 °C",
                "состояние": "Облачно, лёгкий ветер",
            }

        return self.run_with_tools(
            input_text="Какая сейчас погода в Питере?",
            tools=tools,
            handlers={"get_weather": get_weather},
            instructions="Добавляй в ответ подходящие эмоджи.",
        )
