from fastapi import FastAPI
from routers import (
    background_remover,
    image_upscaler,
    shadow_generator,
    logo_generator,
    image_editor
)

app = FastAPI(
    title="Clearify.AI Backend",
    description="AI Tools API for background removal, upscaling, shadows, logos, and editing.",
    version="1.0.0"
)

# Register all routers
app.include_router(background_remover.router, prefix="/api")
app.include_router(image_upscaler.router, prefix="/api")
app.include_router(shadow_generator.router, prefix="/api")
app.include_router(logo_generator.router, prefix="/api")
app.include_router(image_editor.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello, Clearify.AI!"}
