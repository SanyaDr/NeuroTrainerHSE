from typing import List, Dict, Any

from openai import OpenAI

from backend.core.config import settings


class OpenAIClient:
    """Клиент для работы с OpenRouter как с ChatGPT-подобной LLM."""

    def __init__(self) -> None:
        # OpenRouter работает как OpenAI API, только с другим base_url
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
            # эти хедеры не обязательны, но полезны для статистики приложения
            default_headers={
                "HTTP-Referer": "http://localhost:8000",  # можешь потом заменить на прод-URL
                "X-Title": settings.app_name,
            },
        )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai/gpt-4.1-mini",
    ) -> str:
        """
        Отправить список сообщений в модель и вернуть текст ответа.
        Messages: [{"role": "user" / "system" / "assistant", "content": "..."}]
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

# Один общий экземпляр на приложение
openai_client = OpenAIClient()