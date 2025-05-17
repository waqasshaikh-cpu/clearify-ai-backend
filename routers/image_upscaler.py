from fastapi import APIRouter

router = APIRouter()

@router.post("/upscale-image")
async def upscale_image():
    return {"message": "Image upscaled (dummy response)"}
