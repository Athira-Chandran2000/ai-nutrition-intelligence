"""
Hybrid health scoring logic.
Deterministic, explainable, and more realistic.
"""


def calculate_health_score(calories: float, protein: float, carbs: float, fat: float) -> tuple[float, str]:
    score = 10.0

    # Absolute calorie penalties
    if calories > 800:
        score -= 3
    elif calories > 600:
        score -= 2
    elif calories > 450:
        score -= 1

    # Fat penalties
    if fat > 45:
        score -= 3
    elif fat > 35:
        score -= 2
    elif fat > 25:
        score -= 1

    # Carb penalty
    if carbs > 75:
        score -= 1

    # Protein bonus
    if protein >= 30:
        score += 1.5
    elif protein >= 20:
        score += 1

    # Macro ratio analysis
    total_macro_calories = (protein * 4) + (carbs * 4) + (fat * 9)

    if total_macro_calories > 0:
        protein_ratio = (protein * 4) / total_macro_calories
        fat_ratio = (fat * 9) / total_macro_calories

        # Encourage high protein ratio
        if protein_ratio >= 0.30:
            score += 1
        elif protein_ratio < 0.15:
            score -= 1

        # Penalize excessive fat ratio
        if fat_ratio > 0.45:
            score -= 2
        elif fat_ratio > 0.35:
            score -= 1

    # Clamp score
    score = max(0, min(10, round(score, 1)))

    # Recommendation logic
    if score >= 8:
        recommendation = "Excellent macro balance."
    elif score >= 6:
        recommendation = "Reasonably balanced but watch portions."
    elif score >= 4:
        recommendation = "High in fat or calories. Consume in moderation."
    else:
        recommendation = "Nutritionally heavy. Consider lighter alternatives."

    return score, recommendation