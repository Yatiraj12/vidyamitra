"""
Main FastAPI entry point for Vidyamitra
- Loads environment variables
- Registers API routes
- Serves frontend (single-server deployment)
"""

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="Vidyamitra",
    description="AI-powered digital CRP for teachers using RAG",
    version="1.0.0",
)

# Enable CORS (safe defaults)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(chat_router)

# Serve frontend static files
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static",
)

# Serve frontend UI
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))
