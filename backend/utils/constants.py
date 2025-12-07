# backend/utils/constants.py

from typing import Dict, Optional, Literal, TypedDict


# ===== ТИПЫ МЕТРИК ФОРМЫ =====

STRENGTH: str = "strength"
ENDURANCE: str = "endurance"
WELLBEING: str = "wellbeing"

MetricType = Literal["strength", "endurance", "wellbeing"]


class ExercisePointsCfg(TypedDict, total=False):
    """
    Конфиг для одного упражнения.

    type    — какая метрика качается (strength / endurance / wellbeing)
    per_rep — сколько очков за 1 повтор
    per_10s — сколько очков за каждые 10 секунд
    per_30s — сколько очков за каждые 30 секунд
    """
    type: MetricType
    per_rep: int
    per_10s: int
    per_30s: int


# ===== ОЧКИ ЗА УПРАЖНЕНИЯ =====

EXERCISE_POINTS: Dict[str, ExercisePointsCfg] = {
    # ---- СИЛОВЫЕ (strength) — по повторам ----
    "squat":        {"type": STRENGTH, "per_rep": 2},  # приседания
    "lunge":        {"type": STRENGTH, "per_rep": 3},  # выпады
    "pushup":       {"type": STRENGTH, "per_rep": 3},  # отжимания обычные
    "pushup_knees": {"type": STRENGTH, "per_rep": 2},  # отжимания с колен
    "pushup_wall":  {"type": STRENGTH, "per_rep": 1},  # отжимания от стены/стула
    "glute_bridge": {"type": STRENGTH, "per_rep": 2},  # ягодичный мостик
    "crunch":       {"type": STRENGTH, "per_rep": 1},  # скручивания на пресс
    "boat":         {"type": STRENGTH, "per_rep": 2},  # "лодочка"

    # ---- СТАТИКА (strength) — по времени ----
    "plank":      {"type": STRENGTH, "per_10s": 4},  # планка обычная
    "plank_easy": {"type": STRENGTH, "per_10s": 2},  # лёгкая планка (от колен/стены)
    "wall_sit":   {"type": STRENGTH, "per_10s": 3},  # статика в приседе

    # ---- КАРДИО (endurance) — по времени ----
    "run_in_place": {"type": ENDURANCE, "per_10s": 2},  # бег/марш на месте, шаги в стороны
    "jumping_jack": {"type": ENDURANCE, "per_10s": 3},  # джампинг-джеки
    "shadow_box":   {"type": ENDURANCE, "per_10s": 3},  # удары в воздух / бой с тенью
    "burpee":       {"type": ENDURANCE, "per_10s": 5},  # бёрпи – премиум страдания

    # ---- РАСТЯЖКА / ДЫХАНИЕ (wellbeing) — по времени ----
    "stretch":   {"type": WELLBEING, "per_30s": 1},  # любая растяжка
    "breathing": {"type": WELLBEING, "per_30s": 1},  # дыхательные практики
}


def empty_score() -> Dict[str, float]:
    """
    Пустой словарь очков по метрикам, удобно для инициализации.
    """
    return {
        STRENGTH: 0.0,
        ENDURANCE: 0.0,
        WELLBEING: 0.0,
    }


def calculate_exercise_points(
    exercise_id: str,
    reps: Optional[int] = None,
    seconds: Optional[int] = None,
) -> Dict[str, float]:
    """
    Посчитать очки за одно упражнение.

    Возвращает dict:
        {
          "strength": float,
          "endurance": float,
          "wellbeing": float,
        }

    Примеры:
        calculate_exercise_points("squat", reps=15)
        calculate_exercise_points("plank", seconds=30)
        calculate_exercise_points("jumping_jack", seconds=20)
    """
    score = empty_score()
    cfg = EXERCISE_POINTS.get(exercise_id)

    if not cfg:
        # неизвестное упражнение — просто нули
        return score

    metric: MetricType = cfg["type"]

    # Баллы за повторы
    per_rep = cfg.get("per_rep")
    if per_rep is not None and reps is not None:
        score[metric] += float(per_rep * reps)

    # Баллы за время (per_10s)
    per_10s = cfg.get("per_10s")
    if per_10s is not None and seconds is not None:
        units_10s = seconds / 10.0
        score[metric] += float(per_10s) * units_10s

    # Баллы за время (per_30s)
    per_30s = cfg.get("per_30s")
    if per_30s is not None and seconds is not None:
        units_30s = seconds / 30.0
        score[metric] += float(per_30s) * units_30s

    return score


# ===== СЦЕНАРИИ ДЛЯ ПРОГНОЗА ФОРМЫ НА 30 ДНЕЙ =====

FORECAST_SCENARIOS: Dict[str, Dict[str, float | str]] = {
    # Режим паузы — ничего не делаем
    "no_training": {
        "mult": 0.0,
        "label": "Режим паузы",
    },
    # Минималка — короткие, лёгкие сессии
    "minimal": {
        "mult": 0.4,
        "label": "Минималка",
    },
    # По плану — нормальный режим
    "plan": {
        "mult": 1.0,
        "label": "По плану",
    },
    # Турбо — плюс сверх плана
    "turbo": {
        "mult": 1.4,
        "label": "Турбо-режим",
    },
}

# Коэффициенты распада формы (используйте в forecast_engine.py)
DECAY_STRENGTH: float = 0.03
DECAY_ENDURANCE: float = 0.03
DECAY_WELLBEING: float = 0.02

# Базовый "идеальный" дневной прирост при сценарии mult=1.0
BASE_GAIN_STRENGTH: float = 3.0
BASE_GAIN_ENDURANCE: float = 2.5
BASE_GAIN_WELLBEING: float = 1.5
