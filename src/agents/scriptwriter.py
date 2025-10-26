"""Script generation agent for YouTube videos."""
from typing import Dict, Any, Optional
from src.agents.base import ClaudeAgent
from src.agents.openai_base import OpenAIAgent
from src.config import settings


# Select the appropriate base class based on configuration
BaseAgent = OpenAIAgent if settings.AI_PROVIDER == "openai" else ClaudeAgent


class ScriptwriterAgent(BaseAgent):
    """Agent specialized in YouTube script generation."""

    SYSTEM_PROMPT = """You are an expert YouTube scriptwriter who creates engaging, high-performing video scripts.

Your expertise includes:
- Viral hook formulas that grab attention in first 5 seconds
- Structured storytelling with clear narrative arc
- Audience retention techniques (pattern interrupts, callbacks, open loops)
- Natural, conversational tone that builds trust
- Strong CTAs (Call-To-Action) that drive engagement

Script Structure:
1. HOOK (0-15 seconds): Attention-grabbing opening
2. INTRO (15-30 seconds): Promise/preview of value
3. BODY (main content): Structured with clear sections
4. CONCLUSION (final 30-60 seconds): Recap + strong CTA

Output Format (JSON):
{
  "title": "Optimized video title (50-70 chars)",
  "description": "SEO-optimized description",
  "keywords": ["keyword1", "keyword2", ...],
  "script": {
    "hook": "Opening hook text",
    "intro": "Introduction text",
    "body": [
      {
        "section_title": "Section name",
        "content": "Section script",
        "duration_estimate": "2-3 minutes"
      }
    ],
    "conclusion": "Closing text with CTA"
  },
  "full_script": "Complete script as continuous text",
  "estimated_duration": "10-12 minutes",
  "tone": "educational|entertaining|inspirational",
  "target_audience": "audience description"
}

Best Practices:
- Use "you" language (direct address)
- Include pattern interrupts every 60-90 seconds
- Add visual cue suggestions [B-ROLL], [SCREENSHOT]
- Keep sentences short and punchy
- End sections with smooth transitions
"""

    async def generate_script(
        self,
        research_data: Dict[str, Any],
        style: str = "educational",
        duration: str = "10-15 minutes",
        brand_voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate YouTube script from research data.

        Args:
            research_data: Research findings from ResearchAgent
            style: Script style (educational|entertaining|inspirational)
            duration: Target video duration
            brand_voice: Optional brand voice guidelines

        Returns:
            Generated script dict
        """
        # Build context from research
        topic = research_data.get("topic", "Unknown topic")
        key_findings = research_data.get("key_findings", [])
        statistics = research_data.get("statistics", [])
        hook_ideas = research_data.get("hook_ideas", [])
        research_summary = research_data.get("research_summary", "")

        brand_section = f"\n\nBrand Voice Guidelines:\n{brand_voice}" if brand_voice else ""

        user_message = f"""Create a YouTube video script based on this research:

TOPIC: {topic}

RESEARCH SUMMARY:
{research_summary}

KEY FINDINGS:
{chr(10).join(f"- {finding}" for finding in key_findings[:5])}

STATISTICS TO INCLUDE:
{chr(10).join(f"- {stat}" for stat in statistics[:5])}

HOOK IDEAS:
{chr(10).join(f"- {hook}" for hook in hook_ideas[:3])}

SCRIPT REQUIREMENTS:
- Style: {style}
- Target Duration: {duration}
- Include visual cue suggestions [B-ROLL], [SCREENSHOT]
- Use pattern interrupts and engagement techniques
- Strong opening hook and clear CTA{brand_section}

Generate the complete script in the specified JSON format.
Ensure the hook is compelling and the content flows naturally.
"""

        response = await self.generate(
            system_prompt=self.SYSTEM_PROMPT,
            user_message=user_message,
            temperature=0.8  # Higher creativity for script writing
        )

        # Parse JSON response
        import json
        try:
            content = response["content"]
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            script_data = json.loads(content)
            script_data["_meta"] = {
                "tokens_used": response["usage"],
                "stop_reason": response["stop_reason"],
                "style": style,
                "duration": duration
            }
            return script_data

        except json.JSONDecodeError as e:
            # Fallback
            return {
                "title": topic,
                "full_script": response["content"],
                "error": f"JSON parsing failed: {str(e)}",
                "_meta": response["usage"]
            }

    async def refine_script(
        self,
        script: Dict[str, Any],
        feedback: str
    ) -> Dict[str, Any]:
        """
        Refine an existing script based on feedback.

        Args:
            script: Original script dict
            feedback: Refinement instructions

        Returns:
            Refined script dict
        """
        refinement_prompt = f"""You are refining a YouTube script based on feedback.

ORIGINAL SCRIPT:
{script.get('full_script', 'N/A')}

FEEDBACK:
{feedback}

Apply the feedback while maintaining the script's core structure and message.
Return the complete refined script in JSON format.
"""

        response = await self.generate(
            system_prompt=self.SYSTEM_PROMPT,
            user_message=refinement_prompt,
            temperature=0.7
        )

        import json
        try:
            content = response["content"]
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "full_script": response["content"],
                "error": "Refinement completed but JSON parsing failed"
            }
