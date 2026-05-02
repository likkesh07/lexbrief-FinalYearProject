"""
main.py — LexBrief FastAPI Application Entry Point
Run with: uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import get_settings
from routes import analyze, upload, history

# ── App Setup ──────────────────────────────────────────────────────────
settings = get_settings()

app = FastAPI(
    title="LexBrief API",
    description="AI-powered legal document summarizer backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(history.router, prefix="/api", tags=["History"])


# ── Health Check ───────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    return JSONResponse({
        "status": "ok",
        "version": "1.0.0",
        "service": "LexBrief API"
    })


# ── Root ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to LexBrief API",
        "docs": "/docs",
        "health": "/api/health"
    }


# ── Run directly ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
