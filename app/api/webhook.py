from fastapi import APIRouter, Request
from app.controllers import webhook_controller

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.get('')
async def webhook_verify(request: Request):
    return await webhook_controller.verify_webhook(request)

@router.post('')
async def webhook_receive(request: Request):
    return await webhook_controller.receive_webhook(request)
