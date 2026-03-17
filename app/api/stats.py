from fastapi import APIRouter
from app.controllers import stats_controller

router = APIRouter(tags=["stats"])

@router.get('/api/logs')
async def fetch_app_logs():
    return await stats_controller.get_logs_data()

@router.delete('/api/logs')
async def clear_app_logs():
    return await stats_controller.clear_logs_data()

@router.get('/api/stats')
async def get_stats():
    return await stats_controller.get_dashboard_stats()

@router.get('/health')
async def health_check():
    return await stats_controller.health_check()
