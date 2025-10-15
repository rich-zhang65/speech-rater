from fastapi import APIRouter
from app.api.routes import speech

router = APIRouter()

router.include_router(speech.router)
