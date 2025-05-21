from fastapi import APIRouter, UploadFile, File, Body
import base64
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import io

router = APIRouter()

def dummy_logo_image(text, style, color, font, icon):
    # Create a simple logo image with icon + text for demo (replace with AI model in production)
    img = Image.new('RGBA', (512, 256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_obj = ImageFont.truetype('arial.ttf', 48)
    except:
        font_obj = ImageFont.load_default()
    # Draw icon
    draw.text((30, 80), icon, font=font_obj, fill=color)
    # Draw text
    draw.text((110, 80), text, font=font_obj, fill=color)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@router.post("/generate-logo")
async def generate_logo(
    prompt: str = Body(None),
    style: str = Body(None),
    color: str = Body('#1976d2'),
    font: str = Body('Poppins'),
    icon: str = Body('🚀'),
    image: UploadFile = File(None)
):
    try:
        print(f"[DEBUG] /generate-logo: Received request with prompt={prompt}, style={style}, color={color}, font={font}, icon={icon}, image={image.filename if image else None}")
        if prompt:
            img_str = dummy_logo_image(prompt, style or 'modern', color or '#1976d2', font or 'Poppins', icon or '🚀')
            print("[DEBUG] /generate-logo: Generated logo from text.")
            return {"processed_image": img_str}
        elif image:
            image_bytes = await image.read()
            if not image_bytes:
                print("[DEBUG] /generate-logo: No image data received.")
                return {"error": "No image data received."}
            try:
                input_image = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
                print(f"[DEBUG] /generate-logo: Opened image, size: {input_image.size}")
            except UnidentifiedImageError:
                print("[DEBUG] /generate-logo: Uploaded file is not a valid image.")
                return {"error": "Uploaded file is not a valid image."}
            buffered = io.BytesIO()
            input_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            print("[DEBUG] /generate-logo: Returned uploaded image as logo.")
            return {"processed_image": img_str}
        else:
            print("[DEBUG] /generate-logo: No prompt or image provided.")
            return {"error": "No prompt or image provided."}
    except Exception as e:
        print("[ERROR] /generate-logo:", e)
        import traceback
        print(traceback.format_exc())
        return {"error": f"Internal server error: {str(e)}"}
