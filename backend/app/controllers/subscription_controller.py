from fastapi import HTTPException
from app.core.db_helpers import (
    load_subscription, save_subscription, load_token_data, 
    load_reels, get_plan_limits, PLAN_LIMITS
)

async def get_subscription():
    token_data = load_token_data()
    if not token_data:
        # Return default starter plan for unauthenticated users
        return {
            "plan": "starter",
            "is_trial": True,
            "limits": get_plan_limits("starter"),
            "usage": {"reels_used": 0},
        }

    ig_id = token_data["ig_account_id"]
    sub = load_subscription(ig_id)
    reels = load_reels(ig_id)

    return {
        **sub,
        "usage": {
            "reels_used": len(reels),
            "reels_limit": sub["limits"]["max_reels"],
            "can_add_reel": sub["limits"]["max_reels"] == -1 or len(reels) < sub["limits"]["max_reels"],
        }
    }

async def update_subscription(data: dict):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")

    ig_id = token_data["ig_account_id"]
    plan = data.get("plan", "starter")
    
    if plan not in PLAN_LIMITS:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {plan}. Choose starter, pro, or business.")

    # Check if user is first-time for bonus months
    current_sub = load_subscription(ig_id)
    is_first_time = current_sub.get("is_first_time", True) if current_sub else True

    result = save_subscription(ig_id, plan, is_first_time=is_first_time)
    return {
        "status": "success",
        "message": f"Plan updated to {plan}",
        **result
    }

async def get_plans():
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price": 100,
                "currency": "INR",
                "period": "month",
                "trial_days": 7,
                "features": PLAN_LIMITS["starter"],
            },
            {
                "id": "pro",
                "name": "Professional",
                "price": 499,
                "currency": "INR",
                "period": "5 months",
                "bonus_months_first_time": 1,
                "features": PLAN_LIMITS["pro"],
            },
            {
                "id": "business",
                "name": "Business",
                "price": 1149,
                "currency": "INR",
                "period": "10 months",
                "bonus_months_first_time": 2,
                "features": PLAN_LIMITS["business"],
            },
        ]
    }
