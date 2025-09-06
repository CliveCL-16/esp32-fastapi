from fastapi import FastAPI, Request
import os
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(request: Request):
    data = await request.body()  # read raw bytes
    if not data:
        return {"message": "No data received"}

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        f.write(data)

    return {"message": "Uploaded", "path": file_path}
