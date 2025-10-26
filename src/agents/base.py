"""Base Claude agent with tool use capabilities."""
from typing import Any, Dict, List, Optional
from anthropic import Anthropic
from src.config import settings


class ClaudeAgent:
    """Base agent for Claude API interactions."""

    def __init__(self):
        """Initialize Claude client."""
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.MAX_TOKENS

    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 1.0,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from Claude.

        Args:
            system_prompt: System instructions for the agent
            user_message: User's input message
            temperature: Sampling temperature (0-1)
            tools: Optional list of tools for the agent to use

        Returns:
            Response dict with content and optional tool usage
        """
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}]
            }

            if tools:
                kwargs["tools"] = tools

            response = self.client.messages.create(**kwargs)

            return {
                "content": self._extract_content(response),
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "tool_calls": self._extract_tool_calls(response) if tools else None
            }

        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")

    def _extract_content(self, response) -> str:
        """Extract text content from response."""
        for block in response.content:
            if block.type == "text":
                return block.text
        return ""

    def _extract_tool_calls(self, response) -> List[Dict[str, Any]]:
        """Extract tool use calls from response."""
        tool_calls = []
        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
        return tool_calls
