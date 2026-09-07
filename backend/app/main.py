"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health

app = FastAPI(
    title="Real Estate Lead Bot",
    description="PrimeHomes Realty Lead Management System API",
    version="0.1.0",
)

# CORS – tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])


@app.get("/")
async def root():
    return {
        "service": "real-estate-lead-bot",
        "status": "ok",
        "docs": "/docs",
    }
