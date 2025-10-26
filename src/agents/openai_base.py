"""OpenAI agent with similar interface to Claude agent."""
from typing import Any, Dict, List, Optional
from openai import OpenAI
from src.config import settings


class OpenAIAgent:
    """Base agent for OpenAI API interactions."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS

    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 1.0,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from OpenAI.

        Args:
            system_prompt: System instructions for the agent
            user_message: User's input message
            temperature: Sampling temperature (0-2)
            tools: Optional list of tools (not used for now)

        Returns:
            Response dict with content and usage
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=self.max_tokens
            )

            return {
                "content": response.choices[0].message.content,
                "stop_reason": response.choices[0].finish_reason,
                "usage": {
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens
                },
                "tool_calls": None
            }

        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
