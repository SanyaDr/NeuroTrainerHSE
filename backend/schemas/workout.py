# schemas/workout.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum


class VibeMode(str, Enum):
    ANTI_STRESS = "anti_stress"
    RAGE = "rage"
    BOOST = "boost"
    NEUTRAL = "neutral"


class ExerciseStep(BaseModel):
    name: str = Field(..., description="Название упражнения")
    duration_sec: int = Field(..., description="Длительность в секундах")
    difficulty: Literal["easy", "medium", "hard"] = Field("medium")
    instructions: str = Field(..., description="Инструкции по выполнению")
    success_criteria: Optional[str] = Field(None, description="Критерии успеха")


class WorkoutPlan(BaseModel):
    id: Optional[str] = None
    user_id: int
    vibe_mode: VibeMode
    intensity: float = Field(..., ge=0.0, le=1.0, description="Интенсивность 0-1")
    warm_up: List[ExerciseStep]
    main_block: List[ExerciseStep]
    cool_down: List[ExerciseStep]
    estimated_calories: int
    total_duration_min: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    coach_style: str = "balanced"


# === Новая схема ===
class CompleteExerciseRequest(BaseModel):
    exercise_slug: str = Field(..., description="Slug упражнения из utils/constants.py")
    reps: Optional[int] = Field(None, ge=0, description="Количество повторов (если упражнение по повторам)")
    seconds: Optional[int] = Field(None, ge=0, description="Количество секунд (если упражнение по времени)")