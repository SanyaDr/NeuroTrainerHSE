from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import vibe, workout, coach, profile, forecast
from app.core.config import settings

app = FastAPI(
    title="NeuroCoach Vibe API",
    description="AI-тренер для персонализированных тренировок",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(vibe.router)
app.include_router(workout.router)
app.include_router(coach.router)
app.include_router(profile.router)
app.include_router(forecast.router)

@app.get("/")
async def root():
    return {
        "message": "NeuroCoach Vibe API",
        "status": "running",
        "features": [
            "vibe-based-workouts",
            "ai-coach-commentator",
            "personal-sport-profile",
            "30-day-forecast"
        ]
    }