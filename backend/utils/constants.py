# utils/constants.py

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict


# ===== Базовые типы =====

class ExerciseCategory(str, Enum):
    """Категория упражнения — для фильтрации, статистики и т.п."""
    STRENGTH = "strength"                 # силовые по повторам
    STRENGTH_ENDURANCE = "strength_mix"   # статика/пресс по времени
    ENDURANCE = "endurance"               # кардио
    WELLBEING = "wellbeing"               # растяжка/дыхание


class MeasureType(str, Enum):
    """Чем измеряется упражнение."""
    REPS = "reps"     # считаем повторы
    TIME = "time"     # считаем секунды


@dataclass(frozen=True)
class ExerciseConfig:
    """
    Описание упражнения и правил начисления очков.
    - measure_type:
        REPS  -> передаём количество повторов
        TIME  -> передаём количество секунд
    - points_per_unit:
        REPS -> очков за 1 повтор
        TIME -> очков за один интервал времени (seconds_per_unit)
    """
    slug: str
    label: str              # Человеческое название
    emoji: str
    category: ExerciseCategory
    measure_type: MeasureType
    points_per_unit: int
    seconds_per_unit: Optional[int] = None  # только для TIME-упражнений


# ===== Список всех упражнений =====
# slug — строковый id, который ты будешь использовать в коде/БД

EXERCISES: Dict[str, ExerciseConfig] = {
    # --- 1. Силовые (strength), считаем за 1 повтор ---

    "squat": ExerciseConfig(
        slug="squat",
        label="Приседания",
        emoji="🦵",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=2,  # 2 балла за 1 повтор
    ),
    "lunge": ExerciseConfig(
        slug="lunge",
        label="Выпады",
        emoji="🦵",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=3,  # 3 балла за 1 повтор
    ),
    "pushup_standard": ExerciseConfig(
        slug="pushup_standard",
        label="Отжимания обычные",
        emoji="💪",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=3,
    ),
    "pushup_knees": ExerciseConfig(
        slug="pushup_knees",
        label="Отжимания с колен",
        emoji="💪",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=2,
    ),
    "pushup_wall": ExerciseConfig(
        slug="pushup_wall",
        label="Отжимания от стены/стула",
        emoji="💪",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=1,
    ),
    "glute_bridge": ExerciseConfig(
        slug="glute_bridge",
        label="Ягодичный мостик",
        emoji="🍑",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=2,
    ),
    "chair_dips": ExerciseConfig(
        slug="chair_dips",
        label="Обратные отжимания от стула",
        emoji="🧱",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=3,
    ),
    "crunch": ExerciseConfig(
        slug="crunch",
        label="Скручивания на пресс",
        emoji="📦",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=1,
    ),
    "boat": ExerciseConfig(
        slug="boat",
        label="Упражнение «Лодочка»",
        emoji="🛶",
        category=ExerciseCategory.STRENGTH,
        measure_type=MeasureType.REPS,
        points_per_unit=2,
    ),

    # --- 2. Статика и пресс по времени (strength/endurance mix) ---
    # Считаем ЗА КАЖДЫЕ 10 СЕКУНД

    "plank": ExerciseConfig(
        slug="plank",
        label="Планка (обычная)",
        emoji="🧱",
        category=ExerciseCategory.STRENGTH_ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,     # интервал 10 секунд
        points_per_unit=4,       # 4 балла / 10 сек
    ),
    "plank_easy": ExerciseConfig(
        slug="plank_easy",
        label="Планка облегчённая (от колен/у стены)",
        emoji="🧱",
        category=ExerciseCategory.STRENGTH_ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=2,       # 2 балла / 10 сек
    ),
    "wall_sit": ExerciseConfig(
        slug="wall_sit",
        label="Статический присед (сидим внизу)",
        emoji="🧘",
        category=ExerciseCategory.STRENGTH_ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=3,       # 3 балла / 10 сек
    ),

    # --- 3. Кардио (endurance) ---
    # Считаем ЗА КАЖДЫЕ 10 СЕКУНД

    "run_in_place": ExerciseConfig(
        slug="run_in_place",
        label="Бег/марш на месте",
        emoji="🏃",
        category=ExerciseCategory.ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=2,       # 2 балла / 10 сек
    ),
    "jumping_jacks": ExerciseConfig(
        slug="jumping_jacks",
        label="Джампинг-джеки",
        emoji="⭐",
        category=ExerciseCategory.ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=3,       # 3 балла / 10 сек
    ),
    "shadow_boxing": ExerciseConfig(
        slug="shadow_boxing",
        label="Удары в воздух / бой с тенью",
        emoji="🥊",
        category=ExerciseCategory.ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=3,       # 3 балла / 10 сек
    ),
    "burpee": ExerciseConfig(
        slug="burpee",
        label="Бёрпи",
        emoji="💀",
        category=ExerciseCategory.ENDURANCE,
        measure_type=MeasureType.TIME,
        seconds_per_unit=10,
        points_per_unit=5,       # 5 баллов / 10 сек
    ),

    # --- 4. Растяжка и дыхание (wellbeing) ---
    # Считаем ЗА КАЖДЫЕ 30 СЕКУНД

    "stretching": ExerciseConfig(
        slug="stretching",
        label="Растяжка (ноги/спина/руки)",
        emoji="🤸",
        category=ExerciseCategory.WELLBEING,
        measure_type=MeasureType.TIME,
        seconds_per_unit=30,
        points_per_unit=1,       # 1 балл / 30 сек
    ),
    "breathing": ExerciseConfig(
        slug="breathing",
        label="Дыхательные упражнения",
        emoji="😮‍💨",
        category=ExerciseCategory.WELLBEING,
        measure_type=MeasureType.TIME,
        seconds_per_unit=30,
        points_per_unit=1,       # 1 балл / 30 сек
    ),
}


# ===== Универсальная функция подсчёта очков =====

def calculate_exercise_points(
    slug: str,
    reps: Optional[int] = None,
    seconds: Optional[int] = None,
) -> int:
    """
    Универсальный расчёт очков по slug упражнения.

    Для measure_type == REPS:
        - передаём reps
        - seconds игнорируется
        - формула: reps * points_per_unit

    Для measure_type == TIME:
        - передаём seconds
        - используется только полное количество интервалов
          (10 или 30 секунд, в зависимости от seconds_per_unit):
          units = seconds // seconds_per_unit
          points = units * points_per_unit
    """
    if slug not in EXERCISES:
        raise ValueError(f"Неизвестное упражнение: {slug}")

    cfg = EXERCISES[slug]

    if cfg.measure_type == MeasureType.REPS:
        if reps is None:
            raise ValueError("Для упражнений по повторам нужно передать reps")
        if reps < 0:
            raise ValueError("Количество повторов не может быть отрицательным")
        return reps * cfg.points_per_unit

    # TIME-based
    if seconds is None:
        raise ValueError("Для упражнений по времени нужно передать seconds")
    if seconds < 0:
        raise ValueError("Время не может быть отрицательным")
    if not cfg.seconds_per_unit:
        raise RuntimeError("seconds_per_unit не задан для TIME-упражнения")

    units = seconds // cfg.seconds_per_unit  # считаем только полные интервалы
    return int(units * cfg.points_per_unit)
