"""
Main FastAPI entry point for Vidyamitra
Memory-optimized for Render deployment
"""

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.api.chat import router as chat_router

app = FastAPI(
    title="Vidyamitra",
    description="AI-powered digital CRP for teachers using RAG",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(chat_router, prefix="/api")

# Frontend paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/health", include_in_schema=False)
def health_check():
    return JSONResponse({"status": "ok"})

# 🔥 MEMORY-SAFE WARM-UP (LLM ONLY)
@app.on_event("startup")
def warm_up():
    from app.rag.llm import get_llm

    print("🔥 Warming up LLM only (memory-safe)...")
    get_llm()
    print("✅ Warm-up complete")
