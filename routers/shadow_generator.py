from fastapi import APIRouter

router = APIRouter()

@router.post("/generate-shadow")
async def generate_shadow():
    return {"message": "Shadow generated (dummy response)"}
