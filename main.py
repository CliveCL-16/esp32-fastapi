from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import os
from datetime import datetime
import glob

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

@app.get("/latest")
def get_latest_image():
    files = glob.glob(os.path.join(UPLOAD_DIR, "*.jpg"))
    if not files:
        return {"message": "No images yet"}
    latest_file = max(files, key=os.path.getctime)
    return FileResponse(latest_file, media_type="image/jpeg")
