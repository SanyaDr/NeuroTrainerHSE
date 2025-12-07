from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel
import httpx
import os

router = APIRouter()


class ProfileAnalysisRequest(BaseModel):
    workout_history: List[Dict[str, Any]]
    user_goals: List[str] = []


class ProfileAnalysisResponse(BaseModel):
    user_type: str
    analysis: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    optimal_training_schedule: Dict[str, Any]


async def analyze_profile_with_ai(workout_history: List[Dict], goals: List[str]) -> dict:
    """Анализирует профиль пользователя через AI"""
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not api_key:
        return analyze_profile_fallback(workout_history)

    # Формируем историю для AI
    history_summary = summarize_history(workout_history)

    prompt = f"""Проанализируй спортивный профиль пользователя на основе истории тренировок.

История тренировок:
{history_summary}

Цели пользователя: {', '.join(goals) if goals else 'не указаны'}

Проанализируй и верни JSON:
{{
  "user_type": "тип пользователя (например: новичок, энтузиаст, спортсмен)",
  "analysis": "анализ тренировочных привычек (2-3 предложения)",
  "strengths": ["сильная сторона 1", "сильная сторона 2"],
  "weaknesses": ["слабая сторона 1", "слабая сторона 2"],
  "recommendations": ["рекомендация 1", "рекомендация 2", "рекомендация 3"],
  "optimal_training_schedule": {{
    "frequency": "рекомендуемая частота",
    "duration": "рекомендуемая длительность",
    "intensity": "рекомендуемая интенсивность",
    "coach_style": "рекомендуемый стиль тренера"
  }}
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

                import json
                import re

                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())

        return analyze_profile_fallback(workout_history)

    except Exception:
        return analyze_profile_fallback(workout_history)


def summarize_history(workout_history: List[Dict]) -> str:
    """Суммирует историю тренировок для AI"""
    if not workout_history:
        return "История тренировок пуста."

    total = len(workout_history)
    completed = sum(1 for w in workout_history if w.get("completed", False))
    avg_duration = sum(w.get("duration_min", 0) for w in workout_history) / total

    return f"""
    Всего тренировок: {total}
    Завершено: {completed} ({completed/total*100:.0f}%)
    Средняя длительность: {avg_duration:.0f} минут
    """


def analyze_profile_fallback(workout_history: List[Dict]) -> dict:
    """Резервный анализ профиля"""
    if not workout_history:
        return {
            "user_type": "новичок",
            "analysis": "Пользователь только начинает свой спортивный путь.",
            "strengths": ["готовность начать"],
            "weaknesses": ["нет тренировочного опыта"],
            "recommendations": [
                "Начните с 3 тренировок в неделю по 30 минут",
                "Сфокусируйтесь на базовых упражнениях",
                "Отслеживайте прогресс"
            ],
            "optimal_training_schedule": {
                "frequency": "3 раза в неделю",
                "duration": "30 минут",
                "intensity": "умеренная",
                "coach_style": "balanced"
            }
        }

    return {
        "user_type": "активный пользователь",
        "analysis": "Регулярные тренировки с хорошей вовлеченностью.",
        "strengths": ["регулярность", "настойчивость"],
        "weaknesses": ["возможно требуется разнообразие"],
        "recommendations": [
            "Добавьте новые виды упражнений",
            "Попробуйте разные стили тренировок",
            "Увеличьте интенсивность постепенно"
        ],
        "optimal_training_schedule": {
            "frequency": "4 раза в неделю",
            "duration": "40 минут",
            "intensity": "средняя-высокая",
            "coach_style": "balanced"
        }
    }


@router.post("/profile/analyze", response_model=ProfileAnalysisResponse)
async def analyze_user_profile(request: ProfileAnalysisRequest):
    """Анализирует профиль пользователя через AI"""
    try:
        ai_result = await analyze_profile_with_ai(
            request.workout_history,
            request.user_goals
        )

        return ProfileAnalysisResponse(
            user_type=ai_result.get("user_type", "пользователь"),
            analysis=ai_result.get("analysis", "Анализ профиля"),
            strengths=ai_result.get("strengths", []),
            weaknesses=ai_result.get("weaknesses", []),
            recommendations=ai_result.get("recommendations", []),
            optimal_training_schedule=ai_result.get("optimal_training_schedule", {})
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))