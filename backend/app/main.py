from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.routers import router

app = FastAPI(
    title="Speech Rater API",
    description="API for analyzing and grading speech quality",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return JSONResponse(content={
        "message": "Speech Rater API",
        "version": "1.0.0",
        "status": "operational"
    })


@app.get("/ping")
async def ping():
    return JSONResponse(content={"message": "pong"})


# Include API routes
app.include_router(router, prefix="/api")

