from enum import Enum
from typing import Optional
from app.ai.llm_provider import LLMProvider
from app.schemas.workout import VibeMode

class VibeAnalyzer:
    def __init__(self):
        self.llm = LLMProvider()

    async def analyze_from_text(self, text: Optional[str], audio_url: Optional[str]):
        """
        Анализирует текстовое или голосовое описание состояния
        """
        prompt = f"""
        Проанализируй состояние пользователя и определи один из режимов:
        - anti_stress: усталость, стресс, нужна мягкая восстановительная тренировка
        - rage: агрессия, злость, нужна интенсивная силовая/кардио нагрузка
        - boost: хорошее настроение, энергия, можно дать сложную тренировку
        - neutral: нормальное состояние, стандартная тренировка
        
        Описание пользователя: {text}
        
        Верни JSON: {{"mode": "anti_stress|rage|boost|neutral", "confidence": 0.85, "description": "описание", "recommended_intensity": 0.7}}
        """

        response = await self.llm.generate_json(prompt)
        return response
    