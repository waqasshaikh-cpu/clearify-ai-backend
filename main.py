from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Backend server is starting at http://localhost:8000 ...\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
