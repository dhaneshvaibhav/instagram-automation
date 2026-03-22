from fastapi import APIRouter
from app.controllers import subscription_controller

router = APIRouter(prefix="/api/subscription", tags=["subscription"])

@router.get('')
async def get_subscription():
    return await subscription_controller.get_subscription()

@router.post('')
async def update_subscription(data: dict):
    return await subscription_controller.update_subscription(data)

@router.get('/plans')
async def get_plans():
    return await subscription_controller.get_plans()
