from fastapi import APIRouter, HTTPException
from typing import Literal
from pydantic import BaseModel, Field
import httpx

from backend.core.config import settings  # <-- вот это важно

router = APIRouter(prefix="/coach", tags=["coach"])


class CoachCommentRequest(BaseModel):
    style: Literal["strict", "soft", "comedy", "anime", "balanced"]
    exercise: str
    success: bool
    user_progress: float = Field(0.0, ge=0.0, le=1.0)
    additional_context: str = ""


class CoachCommentResponse(BaseModel):
    comment: str
    style: str


async def generate_coach_comment_with_ai(
        style: str,
        exercise: str,
        success: bool,
        progress: float,
        context: str = ""
) -> str:
    """Генерирует комментарий тренера через AI"""
    api_key = settings.openrouter_api_key  # <-- а не os.getenv

    if not api_key:
        return generate_fallback_comment(style, success)

    style_descriptions = {
        "strict": "Ты строгий армейский инструктор. Говори кратко, жёстко, по делу.",
        "soft": "Ты заботливый поддерживающий друг. Подбадриваешь мягко и тепло.",
        "comedy": "Ты юмористический комментатор. Шутишь, но при этом мотивируешь.",
        "anime": "Ты аниме-сенсей. Говоришь драматично, с японскими терминами.",
        "balanced": "Ты профессиональный тренер. Даёшь сбалансированные комментарии."
    }

    prompt = f"""{style_descriptions.get(style, 'Ты тренер.')}

Упражнение: {exercise}
Результат: {"Успешно выполнено" if success else "Нужно улучшить"}
Прогресс пользователя: {progress*100}%
Контекст: {context}

Сгенерируй одну короткую реплику тренера (до 10 слов) для этого момента.
Только реплику, без пояснений."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "@preset/neuro-trainer",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 50
                }
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()

        return generate_fallback_comment(style, success)

    except Exception:
        return generate_fallback_comment(style, success)


def generate_fallback_comment(style: str, success: bool) -> str:
    """Резервный комментарий"""
    if success:
        if style == "strict":
            return "Так держать!"
        elif style == "soft":
            return "Молодец, продолжай!"
        elif style == "comedy":
            return "Отлично! Почти как профи!"
        elif style == "anime":
            return "Субарасии! (Потрясающе!)"
        else:
            return "Хорошо выполнено."
    else:
        if style == "strict":
            return "Повторить!"
        elif style == "soft":
            return "Ничего, попробуй еще раз!"
        elif style == "comedy":
            return "Эх, почти получилось!"
        elif style == "anime":
            return "Гамбаттэ! (Не сдавайся!)"
        else:
            return "Нужно поработать над техникой."


@router.post("/coach/comment", response_model=CoachCommentResponse)
async def get_coach_comment(request: CoachCommentRequest):
    """Генерирует мотивационный комментарий через AI"""
    try:
        comment = await generate_coach_comment_with_ai(
            style=request.style,
            exercise=request.exercise,
            success=request.success,
            progress=request.user_progress,
            context=request.additional_context
        )

        return CoachCommentResponse(
            comment=comment,
            style=request.style
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))