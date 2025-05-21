from fastapi import APIRouter, UploadFile, File
import base64
from PIL import Image, UnidentifiedImageError
import io
import traceback

router = APIRouter()

@router.post("/generate-shadow")
async def generate_shadow(
    image: UploadFile = File(...),
    style: str = File(None),
    angle: str = File(None),
    blur: str = File(None),
    color: str = File(None),
    opacity: str = File(None)
):
    try:
        image_bytes = await image.read()
        if not image_bytes:
            return {"error": "No image data received."}
        try:
            input_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
        except UnidentifiedImageError:
            return {"error": "Uploaded file is not a valid image."}
        # Placeholder for shadow logic (replace with real shadow generation)
        output_image = input_image
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"processed_image": img_str}
    except Exception as e:
        print("[ERROR] /generate-shadow:", e)
        print(traceback.format_exc())
        return {"error": f"Internal server error: {str(e)}"}
