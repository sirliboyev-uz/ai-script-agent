"""Analytics service for dashboard metrics."""
from typing import Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.models.database import Script


class AnalyticsService:
    """Service for analytics and metrics."""

    async def get_dashboard_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Get dashboard statistics.

        Returns:
            Dashboard metrics including counts, averages, and trends
        """
        # Total scripts count
        total_result = await db.execute(select(func.count(Script.id)))
        total_scripts = total_result.scalar() or 0

        # Scripts this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_result = await db.execute(
            select(func.count(Script.id)).where(Script.created_at >= week_ago)
        )
        scripts_this_week = week_result.scalar() or 0

        # Average generation time
        avg_time_result = await db.execute(
            select(func.avg(Script.generation_time)).where(
                Script.generation_time.isnot(None)
            )
        )
        avg_generation_time = avg_time_result.scalar() or 0

        # Total tokens used
        tokens_result = await db.execute(
            select(func.sum(Script.tokens_used)).where(
                Script.tokens_used.isnot(None)
            )
        )
        total_tokens = tokens_result.scalar() or 0

        # Most used style
        style_result = await db.execute(
            select(Script.style, func.count(Script.id).label('count'))
            .group_by(Script.style)
            .order_by(func.count(Script.id).desc())
            .limit(1)
        )
        style_row = style_result.first()
        most_used_style = style_row[0] if style_row else "educational"

        return {
            "total_scripts": total_scripts,
            "scripts_this_week": scripts_this_week,
            "avg_generation_time": round(avg_generation_time, 1) if avg_generation_time else 0,
            "total_tokens": total_tokens,
            "most_used_style": most_used_style,
            "estimated_cost": round(total_tokens / 1000 * 0.01, 2)  # Rough estimate
        }

    async def get_recent_scripts(
        self,
        db: AsyncSession,
        limit: int = 5
    ) -> list:
        """Get recent scripts for dashboard."""
        result = await db.execute(
            select(Script)
            .order_by(Script.created_at.desc())
            .limit(limit)
        )
        scripts = result.scalars().all()

        return [
            {
                "script_id": s.script_id,
                "topic": s.topic,
                "title": s.title,
                "style": s.style,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "tokens_used": s.tokens_used or 0,
                "generation_time": round(s.generation_time, 1) if s.generation_time else 0
            }
            for s in scripts
        ]
