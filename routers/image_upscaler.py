from fastapi import APIRouter, UploadFile, File, Form
import base64
from PIL import Image, UnidentifiedImageError
import io
import traceback

router = APIRouter()

# Map upscale options to scale factors or target sizes
UPSCALE_MAP = {
    '2x': 2,
    '4x': 4,
    '8x': 8,
    '4k': (3840, 2160),
    '8k': (7680, 4320),
}

@router.post("/upscale-image")
async def upscale_image(
    image: UploadFile = File(...),
    upscale: str = Form('2x')
):
    try:
        print(f"[DEBUG] /upscale-image: Received request with upscale={upscale}")
        print(f"[DEBUG] /upscale-image: Received image filename: {image.filename}, content_type: {image.content_type}")
        image_bytes = await image.read()
        print(f"[DEBUG] /upscale-image: Image bytes length: {len(image_bytes) if image_bytes else 0}")
        if not image_bytes:
            print("[DEBUG] /upscale-image: No image data received.")
            return {"error": "No image data received."}
        try:
            input_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
            print(f"[DEBUG] /upscale-image: Opened image, size: {input_image.size}")
        except UnidentifiedImageError:
            print("[DEBUG] /upscale-image: Uploaded file is not a valid image.")
            return {"error": "Uploaded file is not a valid image."}
        w, h = input_image.size
        print(f"[DEBUG] /upscale-image: Original image size: {w}x{h}")
        # Determine upscale size
        if upscale in ['2x', '4x', '8x']:
            factor = UPSCALE_MAP[upscale]
            new_size = (w * factor, h * factor)
        elif upscale in ['4k', '8k']:
            new_size = UPSCALE_MAP[upscale]
        else:
            new_size = (w * 2, h * 2)  # default 2x
        print(f"[DEBUG] /upscale-image: Upscaled image size: {new_size}")
        upscaled = input_image.resize(new_size, Image.LANCZOS)
        buffered = io.BytesIO()
        upscaled.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print("[DEBUG] /upscale-image: Returning processed image.")
        return {"processed_image": img_str}
    except Exception as e:
        print("[ERROR] /upscale-image:", e)
        print(traceback.format_exc())
        return {"error": f"Internal server error: {str(e)}"}
