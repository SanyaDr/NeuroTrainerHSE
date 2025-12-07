from typing import Literal
from app.ai.llm_provider import LLMProvider

class CoachAI:
    STYLES = {
        "strict": "Ты строгий армейский инструктор. Кратко, жёстко, по делу.",
        "soft": "Ты заботливый поддерживающий друг. Подбадриваешь мягко.",
        "comedy": "Ты юмористический комментатор. Шутишь, но мотивируешь.",
        "anime": "Ты аниме-сенсей. Драматично, с японскими терминами."
    }

    def __init__(self):
        self.llm = LLMProvider()

    async def get_comment(
            self,
            style: Literal["strict", "soft", "comedy", "anime"],
            exercise: str,
            success: bool,
            user_progress: float
    ) -> str:
        """
        Генерирует мотивационную реплику для упражнения
        """
        prompt = f"""
        Стиль тренера: {self.STYLES[style]}
        
        Упражнение: {exercise}
        Результат: {"Успешно выполнено" if success else "Нужно улучшить"}
        Прогресс пользователя: {user_progress*100}%
        
        Сгенерируй одну короткую реплику тренера (до 10 слов) для этого момента.
        """

        return await self.llm.generate_text(prompt)
    