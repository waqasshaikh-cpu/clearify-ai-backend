from fastapi import APIRouter, UploadFile, File, Form
import base64
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io
import traceback

router = APIRouter()

@router.post("/remove-background")
async def remove_background(image: UploadFile = File(...)):
    try:
        print("[DEBUG] /remove-background: Received request")
        image_bytes = await image.read()
        print(f"[DEBUG] /remove-background: Image bytes length: {len(image_bytes) if image_bytes else 0}")
        if not image_bytes:
            print("[DEBUG] /remove-background: No image data received.")
            return {"error": "No image data received."}
        try:
            input_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
            print(f"[DEBUG] /remove-background: Opened image, size: {input_image.size}")
        except UnidentifiedImageError:
            print("[DEBUG] /remove-background: Uploaded file is not a valid image.")
            return {"error": "Uploaded file is not a valid image."}
        # Remove background
        try:
            output_image = remove(input_image)
            print("[DEBUG] /remove-background: Background removed successfully.")
        except Exception as e:
            print(f"[ERROR] /remove-background: rembg failed: {e}")
            print(traceback.format_exc())
            return {"error": f"Background removal failed: {str(e)}"}
        # Save output image to bytes
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print("[DEBUG] /remove-background: Returning processed image.")
        return {"processed_image": img_str}
    except Exception as e:
        print("[ERROR] /remove-background:", e)
        print(traceback.format_exc())
        return {"error": f"Internal server error: {str(e)}"}

@router.post("/upscale-image")
async def upscale_image(
    image: UploadFile = File(...),
    upscale: str = Form('2x')
):
    try:
        image_bytes = await image.read()
        if not image_bytes:
            return {"error": "No image data received."}
        try:
            input_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
        except UnidentifiedImageError:
            return {"error": "Uploaded file is not a valid image."}
        # Actual upscale logic
        w, h = input_image.size
        if upscale == '2x':
            new_size = (w * 2, h * 2)
        elif upscale == '4x':
            new_size = (w * 4, h * 4)
        elif upscale == '8x':
            new_size = (w * 8, h * 8)
        elif upscale == '4k':
            new_size = (3840, 2160)
        elif upscale == '8k':
            new_size = (7680, 4320)
        else:
            new_size = (w * 2, h * 2)
        output_image = input_image.resize(new_size, Image.LANCZOS)
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"processed_image": img_str}
    except Exception as e:
        print("[ERROR] /upscale-image:", e)
        print(traceback.format_exc())
        return {"error": f"Internal server error: {str(e)}"}
