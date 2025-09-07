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
    # ✅ return the raw image
    return FileResponse(latest_file, media_type="image/jpeg")

# Optional: JSON version with timestamp
@app.get("/latest-info")
def get_latest_image_info(request: Request):
    files = glob.glob(os.path.join(UPLOAD_DIR, "*.jpg"))
    if not files:
        return {"message": "No images yet"}
    latest_file = max(files, key=os.path.getctime)

    filename = os.path.basename(latest_file)
    timestamp = datetime.fromtimestamp(os.path.getctime(latest_file)).strftime("%d-%m-%Y %H:%M:%S")

    base_url = str(request.base_url).rstrip("/")
    return {
        "image_url": f"{base_url}/latest",  # points to raw image
        "filename": filename,
        "timestamp": timestamp
    }
