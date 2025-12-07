from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel, Field
import httpx
import os

router = APIRouter()


class ForecastRequest(BaseModel):
    current_stats: Dict[str, Any]
    planned_workouts: List[Dict[str, Any]]
    consistency_level: float = Field(0.7, ge=0.0, le=1.0)
    user_goals: List[str] = []


class ForecastResponse(BaseModel):
    optimistic_scenario: Dict[str, Any]
    pessimistic_scenario: Dict[str, Any]
    comparison: Dict[str, Any]
    key_milestones: List[Dict[str, Any]]
    recommendations: List[str]


async def generate_forecast_with_ai(
        current_stats: Dict,
        planned_workouts: List[Dict],
        consistency: float,
        goals: List[str]
) -> dict:
    """Генерирует прогноз через AI"""
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not api_key:
        return generate_forecast_fallback(current_stats, consistency)

    prompt = f"""Создай прогноз спортивной формы на 30 дней.

Текущие показатели:
{current_stats}

Планируемые тренировки: {len(planned_workouts)} тренировок
Уровень регулярности: {consistency*100}%
Цели: {', '.join(goals) if goals else 'общее улучшение формы'}

Верни JSON с двумя сценариями:
{{
  "optimistic_scenario": {{
    "description": "если тренироваться по плану",
    "improvements": {{
      "endurance": "+X%",
      "strength": "+X%",
      "flexibility": "+X%",
      "wellbeing": "+X%"
    }},
    "key_achievements": ["достижение 1", "достижение 2"]
  }},
  "pessimistic_scenario": {{
    "description": "если пропускать тренировки",
    "changes": {{
      "endurance": "-X%",
      "strength": "-X%",
      "flexibility": "-X%",
      "wellbeing": "-X%"
    }},
    "risks": ["риск 1", "риск 2"]
  }},
  "comparison": {{
    "difference_description": "разница между сценариями",
    "motivational_message": "мотивационное сообщение"
  }},
  "key_milestones": [
    {{"day": 7, "title": "первая неделя", "description": "описание"}}
  ],
  "recommendations": ["рекомендация 1", "рекомендация 2"]
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
                    "temperature": 0.4
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

        return generate_forecast_fallback(current_stats, consistency)

    except Exception:
        return generate_forecast_fallback(current_stats, consistency)


def generate_forecast_fallback(current_stats: Dict, consistency: float) -> dict:
    """Резервный прогноз"""
    if consistency > 0.7:
        optimistic = {
            "description": "Отличные результаты при регулярных тренировках",
            "improvements": {
                "endurance": "+25%",
                "strength": "+20%",
                "flexibility": "+15%",
                "wellbeing": "+30%"
            },
            "key_achievements": [
                "Улучшение выносливости",
                "Увеличение силы",
                "Повышение энергии"
            ]
        }
    else:
        optimistic = {
            "description": "Хороший прогресс при умеренной регулярности",
            "improvements": {
                "endurance": "+15%",
                "strength": "+10%",
                "flexibility": "+10%",
                "wellbeing": "+20%"
            },
            "key_achievements": [
                "Стабильный прогресс",
                "Улучшение самочувствия"
            ]
        }

    return {
        "optimistic_scenario": optimistic,
        "pessimistic_scenario": {
            "description": "Потеря прогресса при пропусках тренировок",
            "changes": {
                "endurance": "-10%",
                "strength": "-15%",
                "flexibility": "-5%",
                "wellbeing": "-20%"
            },
            "risks": [
                "Потеря мотивации",
                "Снижение формы",
                "Возврат к старым привычкам"
            ]
        },
        "comparison": {
            "difference_description": "Разница в 35-40% в показателях",
            "motivational_message": "Регулярность - ключ к успеху!"
        },
        "key_milestones": [
            {"day": 7, "title": "Первая неделя", "description": "Адаптация организма"},
            {"day": 14, "title": "Две недели", "description": "Первые заметные изменения"},
            {"day": 30, "title": "Месяц", "description": "Значительное улучшение формы"}
        ],
        "recommendations": [
            "Тренируйтесь регулярно",
            "Отслеживайте прогресс",
            "Не пропускайте тренировки"
        ]
    }


@router.post("/forecast/30days", response_model=ForecastResponse)
async def generate_30day_forecast(request: ForecastRequest):
    """Генерирует прогноз на 30 дней через AI"""
    try:
        ai_result = await generate_forecast_with_ai(
            current_stats=request.current_stats,
            planned_workouts=request.planned_workouts,
            consistency=request.consistency_level,
            goals=request.user_goals
        )

        return ForecastResponse(
            optimistic_scenario=ai_result.get("optimistic_scenario", {}),
            pessimistic_scenario=ai_result.get("pessimistic_scenario", {}),
            comparison=ai_result.get("comparison", {}),
            key_milestones=ai_result.get("key_milestones", []),
            recommendations=ai_result.get("recommendations", [])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))