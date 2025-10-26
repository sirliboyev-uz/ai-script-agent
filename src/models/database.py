"""Database models and setup."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config import settings

Base = declarative_base()


class Script(Base):
    """Script storage model."""

    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    script_id = Column(String(36), unique=True, index=True, nullable=False)

    # Input
    topic = Column(String(500), nullable=False)
    style = Column(String(50), default="educational")
    duration = Column(String(50), default="10-15 minutes")

    # Research Data
    research_data = Column(JSON, nullable=True)
    sources = Column(JSON, nullable=True)

    # Script Content
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)
    full_script = Column(Text, nullable=False)
    script_sections = Column(JSON, nullable=True)

    # Metadata
    estimated_duration = Column(String(50), nullable=True)
    tone = Column(String(50), nullable=True)
    target_audience = Column(String(200), nullable=True)

    # Analytics
    tokens_used = Column(Integer, default=0)
    generation_time = Column(Float, nullable=True)  # in seconds

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "script_id": self.script_id,
            "topic": self.topic,
            "style": self.style,
            "duration": self.duration,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "full_script": self.full_script,
            "script_sections": self.script_sections,
            "estimated_duration": self.estimated_duration,
            "tone": self.tone,
            "target_audience": self.target_audience,
            "research_data": self.research_data,
            "sources": self.sources,
            "tokens_used": self.tokens_used,
            "generation_time": self.generation_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Database engine and session
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
