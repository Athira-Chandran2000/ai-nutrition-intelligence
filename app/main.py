"""
Main FastAPI application entry point.
"""

import logging

from fastapi import FastAPI, HTTPException

from app.core.logger import setup_logging
from app.models.nutrition import FoodAnalysisRequest, FoodAnalysisResponse
from app.services.gemini_service import GeminiService
from app.utils.health_score import calculate_health_score

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Nutrition Intelligence API",
    description="Agentic AI-powered nutrition analysis platform",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict:
    """Health check endpoint."""
    return {"message": "AI Nutrition Intelligence API is running"}


@app.post("/analyze-food", response_model=FoodAnalysisResponse)
async def analyze_food(request: FoodAnalysisRequest) -> FoodAnalysisResponse:
    """
    Analyze a food item and return structured nutrition analysis.
    """
    try:
        gemini = GeminiService()
        macros = gemini.analyze_food(request.food_item)

        health_score, recommendation = calculate_health_score(
            macros["calories"],
            macros["protein"],
            macros["carbs"],
            macros["fat"],
        )

        logger.info(f"Food analyzed successfully: {request.food_item}")

        return FoodAnalysisResponse(
            calories=macros["calories"],
            protein=macros["protein"],
            carbs=macros["carbs"],
            fat=macros["fat"],
            health_score=health_score,
            recommendation=recommendation,
        )

    except Exception as exc:
        logger.error(f"Error analyzing food: {request.food_item} | {exc}")
        raise HTTPException(status_code=500, detail="Food analysis failed.")