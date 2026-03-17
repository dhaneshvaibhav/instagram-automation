from fastapi import APIRouter
from app.models.reel import ReelData, ReelUpdate
from app.controllers import reels_controller

router = APIRouter(prefix="/api/reels", tags=["reels"])

@router.get('/instagram')
async def get_instagram_reels():
    return await reels_controller.get_instagram_reels()

@router.post('/test-dm')
async def test_dm_route(data: dict):
    return await reels_controller.test_dm(data)

@router.get('')
async def get_reels():
    return await reels_controller.list_reels()

@router.post('')
async def create_reel(reel: ReelData):
    return await reels_controller.create_reel(reel)

@router.put('/{reel_id}')
async def update_reel(reel_id: str, reel: ReelUpdate):
    return await reels_controller.update_reel(reel_id, reel)

@router.delete('/{reel_id}')
async def delete_reel(reel_id: str):
    return await reels_controller.delete_reel(reel_id)
