"""Expense policy validation tools for the AI agent."""

POLICY_LIMITS = {
    "transport": 50000,
    "meals": 30000,
    "accommodation": 150000,
    "other": 25000,
}


def check_expense_claim(category: str, amount: float) -> dict:
    """Check an expense claim against the simulated company policy."""

    category = category.strip().lower()

    if category not in POLICY_LIMITS:
        return {
            "status": "invalid",
            "message": f"Unknown expense category: {category}",
            "allowed_categories": list(POLICY_LIMITS.keys()),
        }

    if amount <= 0:
        return {
            "status": "invalid",
            "message": "The expense amount must be greater than zero.",
        }

    limit = POLICY_LIMITS[category]
    approved = amount <= limit

    return {
        "status": "within_policy" if approved else "exceeds_policy",
        "category": category,
        "claimed_amount": amount,
        "policy_limit": limit,
        "difference": round(abs(limit - amount), 2),
        "currency": "NGN",
        "message": (
            "The claim is within the simulated company policy."
            if approved
            else "The claim exceeds the simulated company policy limit."
        ),
    }
