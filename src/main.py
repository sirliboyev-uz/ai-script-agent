"""FastAPI application entry point."""
from datetime import datetime
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import init_db, get_db
from src.models.schemas import (
    GenerateScriptRequest,
    ScriptResponse,
    ScriptListResponse,
    HealthResponse
)
from src.services import ScriptService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Initializing database...")
    await init_db()
    print("Validating configuration...")
    settings.validate()
    print("Application started successfully!")
    yield
    # Shutdown
    print("Application shutting down...")


app = FastAPI(
    title="AI Research-to-Video Script Agent",
    description="Automated research and YouTube script generation using Claude AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service instance
script_service = ScriptService()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend interface."""
    html_path = Path(__file__).parent / "templates" / "index.html"
    with open(html_path, "r") as f:
        return f.read()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/generate", response_model=ScriptResponse)
async def generate_script(
    request: GenerateScriptRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a YouTube script from a topic.

    Args:
        request: Script generation request
        db: Database session

    Returns:
        Generated script with metadata
    """
    try:
        result = await script_service.generate_script(
            db=db,
            topic=request.topic,
            style=request.style,
            duration=request.duration,
            research_depth=request.research_depth,
            brand_voice=request.brand_voice
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scripts/{script_id}")
async def get_script(
    script_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a script by ID.

    Args:
        script_id: Script UUID
        db: Database session

    Returns:
        Script data
    """
    try:
        result = await script_service.get_script(db=db, script_id=script_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scripts", response_model=ScriptListResponse)
async def list_scripts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    List all scripts with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of scripts
    """
    try:
        result = await script_service.list_scripts(db=db, skip=skip, limit=limit)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
