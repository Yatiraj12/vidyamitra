"""
Main FastAPI entry point for Vidyamitra
- Loads environment variables
- Registers API routes
- Serves frontend
- Render & Docker compatible
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(chat_router)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Static files
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

# Frontend UI
@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Health check (Render requirement)
@app.get("/health", include_in_schema=False)
def health():
    return JSONResponse({"status": "ok"})

# 🔥 IMPORTANT: Warm-up to avoid blank responses
@app.on_event("startup")
def warm_up():
    print("🔥 Warming up models and vector store...")
    from app.retrieval.vector_store import get_vector_store
    from app.rag.llm import get_llm

    from app.rag.llm import get_llm
    get_llm()
    print("✅ Warm-up complete")
