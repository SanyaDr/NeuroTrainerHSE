from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import httpx
import os

router = APIRouter()


class VibeAssessmentRequest(BaseModel):
    user_input: str
    fatigue_level: Optional[int] = None
    stress_level: Optional[int] = None
    motivation_level: Optional[int] = None


class VibeAssessmentResponse(BaseModel):
    vibe_mode: str  # anti_stress, rage, boost, neutral
    confidence: float
    mood_description: str
    recommended_intensity: float
    coach_style_suggestion: str
    workout_duration_suggestion: int


async def analyze_with_ai(text: str) -> dict:
    """Анализирует состояние пользователя через AI API"""
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Fallback на простую логику, если API ключ не установлен
        return fallback_analysis(text)

    prompt = f"""Проанализируй состояние пользователя и определи режим тренировки:
1. anti_stress - если усталость, стресс, нужна мягкая восстановительная тренировка
2. rage - если агрессия, злость, нужна интенсивная силовая/кардио нагрузка  
3. boost - если хорошее настроение, энергия, можно дать сложную тренировку
4. neutral - если нормальное состояние, стандартная тренировка

Описание пользователя: {text}

Верни JSON: {{
  "mode": "anti_stress|rage|boost|neutral",
  "confidence": 0.85,
  "description": "краткое описание состояния",
  "recommended_intensity": 0.7,
  "coach_style": "strict|soft|comedy|anime|balanced",
  "workout_duration": 30
}}"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                }
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Парсим JSON из ответа AI
                import json
                import re

                # Ищем JSON в тексте ответа
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    ai_result = json.loads(json_match.group())
                    return {
                        "mode": ai_result.get("mode", "neutral"),
                        "confidence": ai_result.get("confidence", 0.7),
                        "description": ai_result.get("description", "Состояние определено"),
                        "intensity": ai_result.get("recommended_intensity", 0.6),
                        "coach_style": ai_result.get("coach_style", "balanced"),
                        "duration": ai_result.get("workout_duration", 30)
                    }

        return fallback_analysis(text)

    except Exception:
        return fallback_analysis(text)


def fallback_analysis(text: str) -> dict:
    """Резервный анализ, если AI недоступен"""
    text_lower = text.lower()

    if any(word in text_lower for word in ["устал", "усталость", "утомлен", "сон"]):
        return {
            "mode": "anti_stress",
            "confidence": 0.8,
            "description": "Обнаружена усталость",
            "intensity": 0.3,
            "coach_style": "soft",
            "duration": 20
        }
    elif any(word in text_lower for word in ["злой", "агрессия", "раздражен", "злость"]):
        return {
            "mode": "rage",
            "confidence": 0.75,
            "description": "Обнаружен стресс",
            "intensity": 0.8,
            "coach_style": "strict",
            "duration": 30
        }
    elif any(word in text_lower for word in ["энергия", "бодр", "отлично", "мотивация"]):
        return {
            "mode": "boost",
            "confidence": 0.85,
            "description": "Высокий уровень энергии",
            "intensity": 0.9,
            "coach_style": "comedy",
            "duration": 45
        }
    else:
        return {
            "mode": "neutral",
            "confidence": 0.6,
            "description": "Нормальное состояние",
            "intensity": 0.6,
            "coach_style": "balanced",
            "duration": 30
        }


@router.post("/vibe/assess", response_model=VibeAssessmentResponse)
async def assess_current_vibe(request: VibeAssessmentRequest):
    """Оценивает состояние пользователя через AI"""
    try:
        result = await analyze_with_ai(request.user_input)

        return VibeAssessmentResponse(
            vibe_mode=result["mode"],
            confidence=result["confidence"],
            mood_description=result["description"],
            recommended_intensity=result["intensity"],
            coach_style_suggestion=result["coach_style"],
            workout_duration_suggestion=result["duration"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

