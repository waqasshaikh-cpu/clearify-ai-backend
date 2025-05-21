from fastapi import APIRouter, UploadFile, File
import base64
from PIL import Image
import io
import traceback

router = APIRouter()

@router.post("/edit-image")
async def edit_image(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        input_image = Image.open(io.BytesIO(image_bytes))
        buffered = io.BytesIO()
        input_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"processed_image": img_str}
    except Exception as e:
        print("[ERROR] /edit-image:", e)
        print(traceback.format_exc())
        return {"error": str(e)}
