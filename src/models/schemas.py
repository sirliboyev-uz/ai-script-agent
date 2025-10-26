"""Pydantic schemas for API validation."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class GenerateScriptRequest(BaseModel):
    """Request schema for script generation."""

    topic: str = Field(..., min_length=5, max_length=500, description="Video topic")
    style: str = Field(default="educational", description="Script style: educational|entertaining|inspirational")
    duration: str = Field(default="10-15 minutes", description="Target video duration")
    research_depth: str = Field(default="medium", description="Research depth: quick|medium|deep")
    brand_voice: Optional[str] = Field(None, description="Optional brand voice guidelines")


class Source(BaseModel):
    """Source information schema."""

    title: str
    url: Optional[str] = None
    credibility: str = "medium"
    key_points: List[str] = []


class ScriptSection(BaseModel):
    """Script section schema."""

    section_title: str
    content: str
    duration_estimate: str


class ScriptResponse(BaseModel):
    """Response schema for generated script."""

    script_id: str
    topic: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: List[str] = []

    # Script content
    hook: Optional[str] = None
    intro: Optional[str] = None
    body: List[Dict[str, Any]] = []
    conclusion: Optional[str] = None
    full_script: str

    # Metadata
    estimated_duration: Optional[str] = None
    tone: Optional[str] = None
    target_audience: Optional[str] = None

    # Research
    sources: List[Dict[str, Any]] = []
    key_findings: List[str] = []

    # Analytics
    tokens_used: int = 0
    generation_time: Optional[float] = None

    created_at: str


class ScriptListResponse(BaseModel):
    """Response schema for script list."""

    total: int
    scripts: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: str


class RefineRequest(BaseModel):
    """Request schema for script refinement."""

    section_name: str = Field(..., description="Section to refine: hook|intro|body|conclusion")
    current_content: str = Field(..., description="Current section content")
    user_feedback: Optional[str] = Field(None, description="User feedback for refinement")


class RegenerateRequest(BaseModel):
    """Request schema for full script regeneration."""

    user_feedback: Optional[str] = Field(None, description="User feedback for improvements")
