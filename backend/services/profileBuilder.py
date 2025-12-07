from typing import Dict, List
from datetime import datetime, timedelta
from app.ai.llm_provider import LLMProvider

class ProfileBuilder:
    def analyze_user_patterns(self, user_id: int, workouts: List[Dict]) -> Dict:
        """
        Анализирует поведенческие паттерны пользователя
        """
        if not workouts:
            return self._get_default_profile()

        # Анализ регулярности
        skip_rate = self._calculate_skip_rate(workouts)
        avg_duration = self._calculate_avg_duration(workouts)
        preferred_time = self._get_preferred_time(workouts)

        # Анализ предпочтений
        favorite_exercises = self._get_favorite_exercises(workouts)
        intensity_preference = self._get_intensity_preference(workouts)

        # Определение типа пользователя
        user_type = self._classify_user_type(
            skip_rate, avg_duration, intensity_preference
        )

        return {
            "user_type": user_type,
            "skip_rate": skip_rate,
            "avg_session_min": avg_duration,
            "preferred_time": preferred_time,
            "favorite_exercises": favorite_exercises[:5],
            "recommended_coach_style": self._recommend_coach_style(user_type),
            "optimal_session_length": self._calculate_optimal_length(skip_rate, avg_duration)
        }

    def _classify_user_type(self, skip_rate: float, duration: float, intensity: float) -> str:
        if skip_rate > 0.4:
            return "sporadic_enthusiast"
        elif duration < 20:
            return "quick_session_lover"
        elif intensity > 0.7:
            return "intensity_seeker"
        else:
            return "balanced_trainee"