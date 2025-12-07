from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

class VibeMode(str, Enum):
    ANTI_STRESS = "anti_stress"
    RAGE = "rage"
    BOOST = "boost"
    NEUTRAL = "neutral"

class ExerciseStep(BaseModel):
    name: str
    duration_sec: int
    difficulty: str
    instructions: str
    success_criteria: Optional[str] = None

class WorkoutPlan(BaseModel):
    id: Optional[str] = None
    user_id: int
    vibe_mode: VibeMode
    intensity: float  # 0.0 to 1.0
    warm_up: List[ExerciseStep]
    main_block: List[ExerciseStep]
    cool_down: List[ExerciseStep]
    estimated_calories: int
    total_duration_min: int
    generated_at: datetime = datetime.utcnow()
    coach_style: str = "balanced"