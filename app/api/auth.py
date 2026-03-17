from fastapi import APIRouter, Query
from app.controllers import auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get('/login')
async def auth_login():
    return await auth_controller.login()

@router.get('/callback')
async def auth_callback(
    code: str = Query(None),
    error: str = Query(None),
    error_reason: str = Query(None)
):
    return await auth_controller.callback(code, error, error_reason)

@router.get('/status')
async def auth_status():
    return await auth_controller.get_status()

@router.get('/refresh-token')
async def refresh_token_route():
    return await auth_controller.refresh_token()

@router.get('/logout')
async def auth_logout():
    return await auth_controller.logout()
