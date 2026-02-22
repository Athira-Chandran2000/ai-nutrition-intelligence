"""
Gemini AI service using REST-compatible google-genai client.
"""

from google.genai import Client
from app.core.config import settings


class GeminiService:
    """Handles interaction with Gemini API."""

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = Client(api_key=settings.GEMINI_API_KEY)

    def generate_response(self, prompt: str) -> str:
        """Generate AI response from Gemini."""
        response = self.client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
        )

        if not response.candidates:
            raise ValueError("No response from Gemini.")

        return response.candidates[0].content.parts[0].text