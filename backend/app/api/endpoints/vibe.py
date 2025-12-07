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
    try:
        analyzer = VibeAnalyzer()

        if user_input:
            # Анализ текста через AI
            result = await analyzer.analyze_from_text(user_input)
        else:
            # Анализ по числовым оценкам
            result = analyzer.analyze_from_scores(
                fatigue_level, stress_level, motivation_level
            )

        return {
            "success": True,
            "vibe_mode": result.mode,
            "confidence": result.confidence,
            "mood_description": result.description,
            "recommended_intensity": result.recommended_intensity
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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