"""Research agent with web search synthesis."""
from typing import Dict, List, Any
from src.agents.base import ClaudeAgent
from src.agents.openai_base import OpenAIAgent
from src.config import settings


# Select the appropriate base class based on configuration
BaseAgent = OpenAIAgent if settings.AI_PROVIDER == "openai" else ClaudeAgent


class ResearchAgent(BaseAgent):
    """Agent specialized in research and web search synthesis."""

    SYSTEM_PROMPT = """You are an expert research assistant specializing in gathering and synthesizing information for YouTube video scripts.

Your responsibilities:
1. Conduct thorough research on the given topic
2. Synthesize findings from multiple credible sources
3. Extract key facts, statistics, and insights
4. Identify trending angles and hooks
5. Note important citations and sources

Output Format (JSON):
{
  "topic": "original topic",
  "key_findings": ["finding 1", "finding 2", ...],
  "statistics": ["stat 1 with source", "stat 2 with source", ...],
  "trending_angles": ["angle 1", "angle 2", ...],
  "hook_ideas": ["hook 1", "hook 2", ...],
  "sources": [
    {
      "title": "source title",
      "url": "source url",
      "credibility": "high|medium|low",
      "key_points": ["point 1", "point 2"]
    }
  ],
  "research_summary": "2-3 sentence overview of findings"
}

Focus on:
- Factual accuracy and credible sources
- Current trends and recent information
- Practical, actionable insights
- Engaging angles for video content
"""

    async def research_topic(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """
        Research a topic and synthesize findings.

        Args:
            topic: The research topic
            depth: Research depth (quick|medium|deep)

        Returns:
            Research findings dict
        """
        depth_instructions = {
            "quick": "Focus on 2-3 top sources with key highlights",
            "medium": "Gather 4-6 diverse sources with comprehensive analysis",
            "deep": "Conduct extensive research with 8-10 sources, detailed fact-checking"
        }

        user_message = f"""Research the following topic for a YouTube video:

Topic: {topic}

Research Depth: {depth} - {depth_instructions.get(depth, depth_instructions['medium'])}

Provide comprehensive research findings in the specified JSON format.
Ensure all statistics and claims include source attribution.
"""

        response = await self.generate(
            system_prompt=self.SYSTEM_PROMPT,
            user_message=user_message,
            temperature=0.7
        )

        # Parse JSON response
        import json
        try:
            # Extract JSON from response (handle markdown code blocks)
            content = response["content"]
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            research_data = json.loads(content)
            research_data["_meta"] = {
                "tokens_used": response["usage"],
                "stop_reason": response["stop_reason"]
            }
            return research_data

        except json.JSONDecodeError as e:
            # Fallback: return raw content if JSON parsing fails
            return {
                "topic": topic,
                "research_summary": response["content"],
                "error": f"JSON parsing failed: {str(e)}",
                "_meta": response["usage"]
            }

    async def validate_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate source credibility and relevance.

        Args:
            sources: List of source dicts to validate

        Returns:
            Validated sources with credibility scores
        """
        validation_prompt = """You are a fact-checking expert. Evaluate the credibility of sources.

For each source, assess:
1. Domain authority and reputation
2. Recency of information
3. Author expertise
4. Citation quality

Return credibility score: high|medium|low with brief reasoning.
"""

        sources_text = "\n\n".join([
            f"Source {i+1}:\nTitle: {s.get('title', 'N/A')}\nURL: {s.get('url', 'N/A')}"
            for i, s in enumerate(sources)
        ])

        response = await self.generate(
            system_prompt=validation_prompt,
            user_message=sources_text,
            temperature=0.3
        )

        # For now, return sources with validation notes
        # In production, would parse response and update credibility scores
        for source in sources:
            if "credibility" not in source:
                source["credibility"] = "medium"  # Default

        return sources
