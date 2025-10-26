"""Script refinement service."""
from typing import Dict, Any
from src.agents import ScriptwriterAgent


class RefinementService:
    """Service for script refinement and regeneration."""

    def __init__(self):
        """Initialize service with scriptwriter agent."""
        self.scriptwriter = ScriptwriterAgent()

    async def refine_section(
        self,
        section_name: str,
        current_content: str,
        research_data: Dict[str, Any],
        style: str = "educational",
        duration: str = "10-15 minutes",
        brand_voice: str = None,
        user_feedback: str = None
    ) -> Dict[str, Any]:
        """
        Refine a specific section of the script.

        Args:
            section_name: Name of section to refine (hook, intro, body, conclusion)
            current_content: Current content of the section
            research_data: Research data for context
            style: Script style
            duration: Target duration
            brand_voice: Optional brand voice guidelines
            user_feedback: Optional user feedback for refinement

        Returns:
            Refined section content
        """
        refinement_prompt = self._build_refinement_prompt(
            section_name=section_name,
            current_content=current_content,
            research_data=research_data,
            style=style,
            duration=duration,
            brand_voice=brand_voice,
            user_feedback=user_feedback
        )

        # Use scriptwriter to generate refined section
        result = await self.scriptwriter._generate_with_provider(refinement_prompt)

        return {
            "section_name": section_name,
            "refined_content": result,
            "feedback_applied": user_feedback is not None
        }

    async def regenerate_full_script(
        self,
        research_data: Dict[str, Any],
        style: str,
        duration: str,
        brand_voice: str = None,
        user_feedback: str = None
    ) -> Dict[str, Any]:
        """
        Regenerate entire script with user feedback.

        Args:
            research_data: Research data for context
            style: Script style
            duration: Target duration
            brand_voice: Optional brand voice guidelines
            user_feedback: Optional user feedback for improvements

        Returns:
            Complete regenerated script
        """
        if user_feedback:
            # Add user feedback to brand voice
            enhanced_voice = f"{brand_voice or ''}\n\nUser Feedback to Address: {user_feedback}"
        else:
            enhanced_voice = brand_voice

        # Generate new script
        script_data = await self.scriptwriter.generate_script(
            research_data=research_data,
            style=style,
            duration=duration,
            brand_voice=enhanced_voice
        )

        return script_data

    def _build_refinement_prompt(
        self,
        section_name: str,
        current_content: str,
        research_data: Dict[str, Any],
        style: str,
        duration: str,
        brand_voice: str = None,
        user_feedback: str = None
    ) -> str:
        """Build refinement prompt for section."""
        topic = research_data.get("topic", "Unknown")
        key_findings = "\n".join([f"- {f}" for f in research_data.get("key_findings", [])])

        prompt = f"""Refine the '{section_name}' section of a YouTube video script.

**Topic**: {topic}
**Style**: {style}
**Duration**: {duration}

**Research Context**:
{key_findings}

**Current {section_name.title()} Content**:
{current_content}

"""

        if user_feedback:
            prompt += f"""**User Feedback**:
{user_feedback}

"""

        if brand_voice:
            prompt += f"""**Brand Voice Guidelines**:
{brand_voice}

"""

        prompt += f"""**Task**: Improve the {section_name} section based on:
1. User feedback (if provided)
2. Better alignment with research findings
3. More engaging storytelling
4. Stronger audience connection
5. Professional YouTube scriptwriting standards

Provide ONLY the refined {section_name} content, no explanations or meta-commentary.
"""

        return prompt


refinement_service = RefinementService()
