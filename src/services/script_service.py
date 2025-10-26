"""Business logic for script generation."""
import time
import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.agents import ResearchAgent, ScriptwriterAgent
from src.models.database import Script
from src.utils import (
    validate_topic,
    validate_style,
    validate_duration,
    validate_research_depth,
    validate_brand_voice,
    ScriptGenerationError,
    ResearchError
)


class ScriptService:
    """Service for script generation workflow."""

    def __init__(self):
        """Initialize service with agents."""
        self.researcher = ResearchAgent()
        self.scriptwriter = ScriptwriterAgent()

    async def generate_script(
        self,
        db: AsyncSession,
        topic: str,
        style: str = "educational",
        duration: str = "10-15 minutes",
        research_depth: str = "medium",
        brand_voice: str = None
    ) -> Dict[str, Any]:
        """
        Complete script generation workflow.

        Args:
            db: Database session
            topic: Video topic
            style: Script style
            duration: Target duration
            research_depth: Research depth level
            brand_voice: Optional brand voice guidelines

        Returns:
            Complete script data dict
        """
        # Validate inputs
        validate_topic(topic)
        validate_style(style)
        validate_duration(duration)
        validate_research_depth(research_depth)
        validate_brand_voice(brand_voice)

        start_time = time.time()
        script_id = str(uuid.uuid4())

        try:
            # Step 1: Research
            print(f"[{script_id}] Starting research for: {topic}")
            try:
                research_data = await self.researcher.research_topic(
                    topic=topic,
                    depth=research_depth
                )
            except Exception as e:
                raise ResearchError(f"Research phase failed: {str(e)}")

            # Validate research results
            if not research_data or "error" in research_data:
                raise ResearchError("Failed to gather sufficient research data")

            # Step 2: Generate script
            print(f"[{script_id}] Generating script...")
            try:
                script_data = await self.scriptwriter.generate_script(
                    research_data=research_data,
                    style=style,
                    duration=duration,
                    brand_voice=brand_voice
                )
            except Exception as e:
                raise ScriptGenerationError(f"Script generation failed: {str(e)}")

            # Validate script results
            if not script_data or not script_data.get("full_script"):
                raise ScriptGenerationError("Failed to generate valid script")

            # Calculate total tokens
            research_tokens = research_data.get("_meta", {}).get("tokens_used", {})
            script_tokens = script_data.get("_meta", {}).get("tokens_used", {})

            total_tokens = (
                research_tokens.get("input_tokens", 0) +
                research_tokens.get("output_tokens", 0) +
                script_tokens.get("input_tokens", 0) +
                script_tokens.get("output_tokens", 0)
            )

            generation_time = time.time() - start_time

            # Step 3: Save to database
            script_record = Script(
                script_id=script_id,
                topic=topic,
                style=style,
                duration=duration,
                research_data=research_data,
                sources=research_data.get("sources", []),
                title=script_data.get("title"),
                description=script_data.get("description"),
                keywords=script_data.get("keywords", []),
                full_script=script_data.get("full_script", ""),
                script_sections=script_data.get("script", {}),
                estimated_duration=script_data.get("estimated_duration"),
                tone=script_data.get("tone"),
                target_audience=script_data.get("target_audience"),
                tokens_used=total_tokens,
                generation_time=generation_time
            )

            db.add(script_record)
            await db.commit()
            await db.refresh(script_record)

            print(f"[{script_id}] Script generated successfully in {generation_time:.2f}s")

            # Build response
            return self._build_response(script_record, research_data, script_data)

        except Exception as e:
            await db.rollback()
            print(f"[{script_id}] Error: {str(e)}")
            raise

    async def get_script(self, db: AsyncSession, script_id: str) -> Dict[str, Any]:
        """Get script by ID."""
        result = await db.execute(
            select(Script).where(Script.script_id == script_id)
        )
        script = result.scalar_one_or_none()

        if not script:
            raise ValueError(f"Script {script_id} not found")

        return script.to_dict()

    async def list_scripts(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
    ) -> Dict[str, Any]:
        """List all scripts with pagination."""
        # Get total count
        count_result = await db.execute(select(Script))
        total = len(count_result.all())

        # Get paginated results
        result = await db.execute(
            select(Script)
            .order_by(Script.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        scripts = result.scalars().all()

        return {
            "total": total,
            "scripts": [s.to_dict() for s in scripts]
        }

    def _build_response(
        self,
        script_record: Script,
        research_data: Dict[str, Any],
        script_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build unified response from all data sources."""
        script_sections = script_data.get("script", {})

        return {
            "script_id": script_record.script_id,
            "topic": script_record.topic,
            "title": script_data.get("title"),
            "description": script_data.get("description"),
            "keywords": script_data.get("keywords", []),

            # Script structure
            "hook": script_sections.get("hook") if isinstance(script_sections, dict) else None,
            "intro": script_sections.get("intro") if isinstance(script_sections, dict) else None,
            "body": script_sections.get("body", []) if isinstance(script_sections, dict) else [],
            "conclusion": script_sections.get("conclusion") if isinstance(script_sections, dict) else None,
            "full_script": script_data.get("full_script", ""),

            # Metadata
            "estimated_duration": script_data.get("estimated_duration"),
            "tone": script_data.get("tone"),
            "target_audience": script_data.get("target_audience"),

            # Research
            "sources": research_data.get("sources", []),
            "key_findings": research_data.get("key_findings", []),

            # Analytics
            "tokens_used": script_record.tokens_used,
            "generation_time": script_record.generation_time,

            "created_at": script_record.created_at.isoformat()
        }
