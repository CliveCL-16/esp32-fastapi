import requests
import time
from datetime import datetime
import os

# ESP32 IP address
ESP32_IP = "192.168.1.11"
URL = f"http://{ESP32_IP}/latest.jpg"

# Folder to save images
SAVE_FOLDER = "ESP32_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Keep track of the last saved image
last_saved = None

while True:
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            # Create a unique filename based on timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(SAVE_FOLDER, f"photo_{timestamp}.jpg")

            # Only save if the image changed
            if response.content != last_saved:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Saved new image: {filename}")
                last_saved = response.content
        else:
            print(f"Failed to fetch image, status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(1)  # check every 1 second
