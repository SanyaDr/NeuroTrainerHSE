"""Фича 2.1"""

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.workout import VibeMode
from app.services.vibe_analyzer import VibeAnalyzer
from app.services.workout_gen import WorkoutGenerator

router = APIRouter(prefix="/vibe", tags=["vibe-check"])

@router.post("/assess")
async def assess_current_vibe(
        user_input: str = None,
        audio_url: Optional[str] = None,
        fatigue_level: int = 3,  # 1-5
        stress_level: int = 3,   # 1-5
        motivation_level: int = 3  # 1-5
):
    """
    Анализирует текущее состояние пользователя
    """
    analyzer = VibeAnalyzer()

    # Если есть текст или аудио - анализируем через LLM
    if user_input or audio_url:
        vibe_result = await analyzer.analyze_from_text(user_input, audio_url)
    else:
        # Используем числовые оценки
        vibe_result = analyzer.analyze_from_scores(
            fatigue_level, stress_level, motivation_level
        )

    return {
        "vibe_mode": vibe_result.mode,
        "confidence": vibe_result.confidence,
        "mood_description": vibe_result.description,
        "recommended_intensity": vibe_result.recommended_intensity
    }

@router.post("/generate-workout")
async def generate_workout_from_vibe(
        vibe_mode: VibeMode,
        user_id: int,
        duration_min: int = 30,
        equipment: List[str] = ["bodyweight"]
):
    """
    Генерирует персонализированную тренировку
    """
    generator = WorkoutGenerator()
    workout = await generator.generate(
        user_id=user_id,
        vibe_mode=vibe_mode,
        duration_min=duration_min,
        equipment=equipment
    )

    return workout