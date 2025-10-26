"""Template service for pre-made script templates."""
from typing import Dict, List, Any


class TemplateService:
    """Service for script templates."""

    TEMPLATES = [
        {
            "id": "tutorial",
            "name": "Tutorial/How-To",
            "description": "Step-by-step educational content",
            "icon": "📚",
            "example_topic": "How to start a podcast",
            "style": "educational",
            "duration": "10-15 minutes",
            "research_depth": "medium",
            "brand_voice": "Clear, instructional, beginner-friendly with step-by-step guidance"
        },
        {
            "id": "product-review",
            "name": "Product Review",
            "description": "Honest product analysis",
            "icon": "⭐",
            "example_topic": "iPhone 15 Pro Max Review",
            "style": "entertaining",
            "duration": "8-10 minutes",
            "research_depth": "deep",
            "brand_voice": "Balanced, honest, detailed with pros and cons"
        },
        {
            "id": "vlog",
            "name": "Vlog/Personal Story",
            "description": "Personal narrative content",
            "icon": "🎥",
            "example_topic": "My journey learning web development",
            "style": "inspirational",
            "duration": "5-8 minutes",
            "research_depth": "quick",
            "brand_voice": "Personal, authentic, conversational with storytelling elements"
        },
        {
            "id": "listicle",
            "name": "Top 10/Listicle",
            "description": "Ranked list format",
            "icon": "📊",
            "example_topic": "Top 10 productivity apps in 2024",
            "style": "entertaining",
            "duration": "10-15 minutes",
            "research_depth": "medium",
            "brand_voice": "Engaging, concise, with clear rankings and reasons"
        },
        {
            "id": "explainer",
            "name": "Explainer/Deep Dive",
            "description": "Complex topic breakdown",
            "icon": "🔬",
            "example_topic": "How AI language models work",
            "style": "educational",
            "duration": "15-20 minutes",
            "research_depth": "deep",
            "brand_voice": "Technical yet accessible, using analogies and examples"
        },
        {
            "id": "news-analysis",
            "name": "News/Trend Analysis",
            "description": "Current events commentary",
            "icon": "📰",
            "example_topic": "Latest AI developments explained",
            "style": "educational",
            "duration": "8-10 minutes",
            "research_depth": "deep",
            "brand_voice": "Informative, objective, with context and implications"
        }
    ]

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates."""
        return self.TEMPLATES

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get specific template by ID."""
        for template in self.TEMPLATES:
            if template["id"] == template_id:
                return template
        raise ValueError(f"Template {template_id} not found")

    def apply_template(
        self,
        template_id: str,
        custom_topic: str = None
    ) -> Dict[str, Any]:
        """
        Apply template to generate form data.

        Args:
            template_id: Template identifier
            custom_topic: Optional custom topic override

        Returns:
            Form data with template settings applied
        """
        template = self.get_template(template_id)

        return {
            "topic": custom_topic or template["example_topic"],
            "style": template["style"],
            "duration": template["duration"],
            "research_depth": template["research_depth"],
            "brand_voice": template["brand_voice"]
        }
