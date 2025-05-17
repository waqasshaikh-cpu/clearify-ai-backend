from fastapi import APIRouter

router = APIRouter()

@router.post("/remove-background")
async def remove_background():
    return {"message": "Background removed (dummy response)"}
