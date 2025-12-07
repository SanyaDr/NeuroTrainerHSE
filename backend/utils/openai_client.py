from typing import List, Dict, Any

from openrouter import OpenRouter
from core.config import settings


class OpenAIClient:
    """Клиент для работы с OpenRouter как с ChatGPT-подобной LLM."""

    def __init__(self) -> None:
        self.client = OpenRouter(api_key=settings.openrouter_api_key)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai/gpt-4.1-mini",
    ) -> str:
        """
        Отправить список сообщений в модель и вернуть текст ответа.
        Messages: [{"role": "user" / "system" / "assistant", "content": "..."}]
        """
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        # В SDK message обычно как dict-like объект
        return completion.choices[0].message["content"]


# Один общий экземпляр на приложение
openai_client = OpenAIClient()