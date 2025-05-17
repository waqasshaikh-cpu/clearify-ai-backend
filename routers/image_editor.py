from fastapi import APIRouter

router = APIRouter()

@router.post("/edit-image")
async def edit_image():
    return {"message": "Image edited (dummy response)"}
