from fastapi import APIRouter

router = APIRouter()

@router.post("/generate-logo")
async def generate_logo():
    return {"message": "Logo generated (dummy response)"}
