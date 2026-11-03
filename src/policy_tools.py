"""Expense policy validation tools for the AI agent."""

import math

POLICY_LIMITS = {
    "transport": 50000,
    "meals": 30000,
    "accommodation": 150000,
    "other": 25000,
}


def check_expense_claim(category: str, amount: float) -> dict:
    """Validate an expense against simulated company policy limits."""

    # Validate category
    if not isinstance(category, str) or not category.strip():
        return {
            "status": "invalid",
            "message": "Please provide a valid expense category.",
            "allowed_categories": list(POLICY_LIMITS.keys()),
        }

    category = category.strip().lower()

    if category not in POLICY_LIMITS:
        return {
            "status": "invalid",
            "message": f"Unknown expense category: {category}",
            "allowed_categories": list(POLICY_LIMITS.keys()),
        }

    # Validate amount
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return {
            "status": "invalid",
            "message": "The expense amount must be a valid number.",
        }

    if not math.isfinite(amount) or amount <= 0:
        return {
            "status": "invalid",
            "message": "The expense amount must be greater than zero and finite.",
        }

    limit = POLICY_LIMITS[category]
    within_policy = amount <= limit
    difference = round(abs(limit - amount), 2)

    return {
        "status": "within_policy" if within_policy else "exceeds_policy",
        "category": category,
        "claimed_amount": amount,
        "policy_limit": limit,
        "difference": difference,
        "currency": "NGN",
        "message": (
            "The claim is within the simulated company policy limit. "
            "This does not mean it has been approved or paid."
            if within_policy
            else "The claim exceeds the simulated company policy limit "
                 "and may require further review."
        ),
    }
