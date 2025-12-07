# api/endpoints/workout.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import httpx
import os

from ...schemas.workout import CompleteExerciseRequest  # относительный импорт
from ...utils.constants import calculate_exercise_points, EXERCISES  # относительный импорт
from ...models.user import User  # относительный импорт
from ...core.auth import get_current_user  # относительный импорт
from ...core.database import get_db  # относительный импорт
from sqlalchemy.orm import Session

router = APIRouter()


class WorkoutRequest(BaseModel):
    vibe_mode: str
    duration_min: int = Field(30, ge=10, le=90)
    fitness_level: str = "intermediate"
    equipment: List[str] = ["bodyweight"]
    focus_areas: Optional[List[str]] = None


class Exercise(BaseModel):
    name: str
    duration_sec: int
    instructions: str
    difficulty: str = "medium"


class WorkoutResponse(BaseModel):
    workout_id: str
    vibe_mode: str
    intensity: float
    total_duration_min: int
    estimated_calories: int
    warm_up: List[Exercise]
    main_block: List[Exercise]
    cool_down: List[Exercise]
    generated_at: datetime


async def generate_workout_with_ai(vibe_mode: str, duration: int) -> dict:
    """Генерирует тренировку через AI API"""
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not api_key:
        return generate_fallback_workout(vibe_mode, duration)

    prompt = f"""Сгенерируй план тренировки на {duration} минут для режима: {vibe_mode}

Режимы:
- anti_stress: мягкая восстановительная тренировка, растяжка, дыхательные упражнения
- rage: интенсивная силовая/кардио нагрузка, высокая интенсивность
- boost: энергичная тренировка со сложными упражнениями
- neutral: сбалансированная тренировка, средняя интенсивность

Верни JSON структуру тренировки:
{{
  "intensity": 0.7,
  "estimated_calories": 250,
  "warm_up": [
    {{"name": "название", "duration_sec": 180, "instructions": "описание", "difficulty": "easy"}}
  ],
  "main_block": [
    {{"name": "название", "duration_sec": 300, "instructions": "описание", "difficulty": "medium"}}
  ],
  "cool_down": [
    {{"name": "название", "duration_sec": 180, "instructions": "описание", "difficulty": "easy"}}
  ]
}}"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions  ",
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

        return generate_fallback_workout(vibe_mode, duration)

    except Exception:
        return generate_fallback_workout(vibe_mode, duration)


def generate_fallback_workout(vibe_mode: str, duration: int) -> dict:
    """Резервная генерация тренировки"""
    intensity_map = {
        "anti_stress": 0.3,
        "rage": 0.8,
        "boost": 0.9,
        "neutral": 0.6
    }

    return {
        "intensity": intensity_map.get(vibe_mode, 0.6),
        "estimated_calories": duration * 8,
        "warm_up": [
            {
                "name": "Разминка суставов",
                "duration_sec": 300,
                "instructions": "Вращайте всеми суставами по 10 раз каждым",
                "difficulty": "easy"
            }
        ],
        "main_block": [
            {
                "name": "Основное упражнение",
                "duration_sec": duration * 30,
                "instructions": "Выполняйте в умеренном темпе",
                "difficulty": "medium"
            }
        ],
        "cool_down": [
            {
                "name": "Растяжка",
                "duration_sec": 180,
                "instructions": "Медленно растяните все мышцы",
                "difficulty": "easy"
            }
        ]
    }


@router.post("/workout/generate", response_model=WorkoutResponse)
async def generate_workout(request: WorkoutRequest):
    """Генерирует персонализированную тренировку через AI"""
    try:
        ai_result = await generate_workout_with_ai(request.vibe_mode, request.duration_min)

        workout_id = f"workout_{datetime.now().timestamp():.0f}"

        return WorkoutResponse(
            workout_id=workout_id,
            vibe_mode=request.vibe_mode,
            intensity=ai_result.get("intensity", 0.6),
            total_duration_min=request.duration_min,
            estimated_calories=ai_result.get("estimated_calories", 200),
            warm_up=[Exercise(**ex) for ex in ai_result.get("warm_up", [])],
            main_block=[Exercise(**ex) for ex in ai_result.get("main_block", [])],
            cool_down=[Exercise(**ex) for ex in ai_result.get("cool_down", [])],
            generated_at=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Новый endpoint для завершения упражнения ===
@router.post("/workout/complete_exercise")
async def complete_exercise(
        request: CompleteExerciseRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Принимает выполненное упражнение, вычисляет баллы и обновляет рейтинг пользователя.
    """
    # Проверяем, что упражнение существует
    if request.exercise_slug not in EXERCISES:
        raise HTTPException(status_code=400, detail="Unknown exercise slug")

    cfg = EXERCISES[request.exercise_slug]

    # Проверяем, что переданы правильные поля (reps или seconds)
    reps = request.reps
    seconds = request.seconds

    if cfg.measure_type == "reps" and reps is None:
        raise HTTPException(status_code=400, detail="Field 'reps' is required for this exercise")
    if cfg.measure_type == "time" and seconds is None:
        raise HTTPException(status_code=400, detail="Field 'seconds' is required for this exercise")

    try:
        points = calculate_exercise_points(
            slug=request.exercise_slug,
            reps=reps,
            seconds=seconds
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Обновляем рейтинг пользователя
    current_user.rating += points
    db.commit()
    db.refresh(current_user)

    return {
        "status": "success",
        "points_earned": points,
        "total_rating": current_user.rating
    }