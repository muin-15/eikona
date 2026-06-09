from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
import io
from PIL import Image

app = FastAPI()

# Enable CORS so your React Frontend can talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_image_metadata(img_array, file):
    """Extracts basic details from the NumPy array and original file."""
    h, w, c = img_array.shape
    return {
        "filename": file.filename,
        "width": w,
        "height": h,
        "channels": c,
        "size_kb": round(len(img_array.tobytes()) / 1024, 2),
        "dtype": str(img_array.dtype)
    }

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # 1. Read the uploaded file into memory
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # 2. Extract Details (Metadata)
    metadata = get_image_metadata(img, file)

    # 3. COMPRESSION FOR UI (Standard Lossy Compression)
    # We use WebP or JPEG at 50% quality to make the "Main Window" snappy
    # This is different from the RLE/Huffman tools you will build later.
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, buffer = cv2.imencode('.jpg', img, encode_param)
    
    # 4. Convert to Base64 to send to Frontend
    base64_image = base64.b64encode(buffer).decode('utf-8')
    
    return {
        "metadata": metadata,
        "preview_image": f"data:image/jpeg;base64,{base64_image}",
        "status": "Success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)