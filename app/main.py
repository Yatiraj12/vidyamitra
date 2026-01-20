"""
Main FastAPI entry point for Vidyamitra
- Loads environment variables
- Registers API routes
- Serves frontend (single-server deployment)
- Render / Docker compatible
"""

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.api.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="Vidyamitra",
    description="AI-powered digital CRP for teachers using RAG",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIX: NO PREFIX HERE
app.include_router(chat_router)

# Absolute path handling (Docker / Render safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Serve frontend static assets
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

# Serve frontend UI
@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Health check (Render friendly)
@app.get("/health", include_in_schema=False)
def health_check():
    return JSONResponse({"status": "ok"})
