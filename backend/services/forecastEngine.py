import numpy as np
from datetime import datetime, timedelta

class ForecastEngine:
    def generate_30day_forecast(
            self,
            current_stats: Dict,
            planned_workouts: List,
            user_profile: Dict
    ) -> Dict:
        """
        Генерирует два сценария на 30 дней
        """
        baseline = {
            "endurance": current_stats.get("endurance", 50),
            "strength": current_stats.get("strength", 50),
            "wellbeing": current_stats.get("wellbeing", 50),
            "consistency": current_stats.get("consistency", 0)
        }

        # Сценарий 1: Тренируюсь по плану
        positive_scenario = self._simulate_progress(
            baseline, planned_workouts, user_profile
        )

        # Сценарий 2: Забиваю
        negative_scenario = self._simulate_regression(baseline)

        return {
            "current_self": baseline,
            "future_consistent": positive_scenario,
            "future_skip": negative_scenario,
            "comparison": self._calculate_comparison(positive_scenario, negative_scenario)
        }

    def _simulate_progress(self, baseline, workouts, profile):
        """
        Моделирует прогресс с учетом тренировок
        """
        # Упрощенная модель прогресса
        endurance_gain = 0.5  # % за тренировку
        strength_gain = 0.3   # % за тренировку

        result = baseline.copy()
        for workout in workouts:
            if workout.get("completed", False):
                result["endurance"] += endurance_gain * workout.get("intensity", 1)
                result["strength"] += strength_gain * workout.get("intensity", 1)
                result["wellbeing"] += 0.2
                result["consistency"] += 1

        return result