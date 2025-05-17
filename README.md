# Clearify AI Backend

AI-powered backend for Clearify.AI providing APIs for background removal, image upscaling, shadow generation, logo creation, and image editing.

## Features

- Background Remover API
- Image Upscaler API
- Shadow Generator API
- Logo Generator API
- Image Editor API

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/clearify-ai-backend.git
   cd clearify-ai-backend
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```sh
   uvicorn main:app --reload
   ```

4. **Open API docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Project Structure

```
clearify-ai-backend/
├── main.py
├── requirements.txt
├── .gitignore
└── routers/
    ├── __init__.py
    ├── background_remover.py
    ├── image_upscaler.py
    ├── shadow_generator.py
    ├── logo_generator.py
    └── image_editor.py
```

## License

MIT