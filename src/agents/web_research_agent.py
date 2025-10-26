"""Research agent using OpenAI Agents SDK with real web search."""
import json
from typing import Dict, Any
from agents import Agent, WebSearchTool, Runner


class WebResearchAgent:
    """Agent specialized in web research using OpenAI Agents SDK."""

    def __init__(self):
        """Initialize the web research agent with search capabilities."""
        self.agent = Agent(
            name="Research Assistant",
            instructions="""You are an expert research assistant specializing in gathering and synthesizing information for YouTube video scripts.

Your responsibilities:
1. Conduct thorough web research on the given topic using the web search tool
2. Synthesize findings from multiple credible sources
3. Extract key facts, statistics, and insights
4. Identify trending angles and hooks
5. Note important citations and sources with real URLs from your searches

When researching:
- Use the web search tool to find current, reliable information
- Search multiple queries to get diverse perspectives
- Prioritize authoritative sources
- Extract specific statistics and data points with source URLs
- Look for trending discussions and angles
- Identify compelling hooks for video content

IMPORTANT: You MUST return your findings in valid JSON format exactly as shown below.

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
- Factual accuracy with real source URLs
- Current trends and recent information (2024-2025)
- Practical, actionable insights
- Engaging angles for video content
""",
            tools=[WebSearchTool()],
        )

    async def research_topic(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """
        Research a topic using web search and synthesize findings.

        Args:
            topic: The research topic
            depth: Research depth (quick|medium|deep)

        Returns:
            Research findings dict
        """
        depth_instructions = {
            "quick": "Focus on 2-3 top sources with key highlights. Be concise.",
            "medium": "Gather 4-6 diverse sources with comprehensive analysis",
            "deep": "Conduct extensive research with 8-10 sources, detailed fact-checking"
        }

        user_message = f"""Research the following topic for a YouTube video:

Topic: {topic}

Research Depth: {depth} - {depth_instructions.get(depth, depth_instructions['medium'])}

Steps to follow:
1. Use web search to find current, authoritative information about this topic
2. Search for multiple queries to get diverse perspectives (e.g., "{topic}", "{topic} trends 2025", "{topic} statistics", "{topic} latest news")
3. Analyze the search results and extract key information
4. Synthesize findings into the JSON format specified in your instructions

Provide comprehensive research findings in the specified JSON format.
Ensure all statistics and claims include source attribution with URLs from your search results.
"""

        # Run the agent with the runner (using the correct API)
        result = await Runner.run(self.agent, user_message)

        # Extract the response from final_output
        response_text = result.final_output if hasattr(result, 'final_output') else str(result)

        # Parse JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                research_data = json.loads(json_str)
            else:
                # If no JSON found, create structured response from text
                research_data = {
                    "topic": topic,
                    "key_findings": [response_text[:500]],
                    "statistics": [],
                    "trending_angles": [],
                    "hook_ideas": [],
                    "sources": [],
                    "research_summary": response_text[:200]
                }
        except json.JSONDecodeError:
            # Fallback: create basic structure
            research_data = {
                "topic": topic,
                "key_findings": [response_text[:500]],
                "statistics": [],
                "trending_angles": [],
                "hook_ideas": [],
                "sources": [],
                "research_summary": response_text[:200]
            }

        return research_data
