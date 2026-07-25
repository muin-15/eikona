# Backend
Backend of Eikona consist of Traditional FastAPI endpoints with opencv for Image processing and Algorithms as YOLO and YuNet

---

## Backend Structure

```
backend_eikona/
├─ .python-version
├─ app
│  ├─ main.py
│  ├─ models/
│  │  └─ face_detection_yunet_2023mar.onnx
│  └─ yolo11n.pt
├─ requirements.txt
├─ runtime.txt
└─ Readme.md
```

---

## Installation

### Clone
```bash
git clone https://github.com/muin-15/eikona.git
cd eikona/backend_eikona
```

### Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server
```bash
uvicorn app.main:app --reload
```
Default Url

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Modules

|Module|Description|
|-------|-----------|
|Operations|Add,Sub,Multiply,Division|
|Color Conversion|Convert Between Color Spaces|
|Transformations|Rotate,Resize,Log,Power Law,Negative|
|Filtering|Blur,Sharpening,Smoothing|
|Restoration|Wiener & Inverse Filter|
|Analytics|Histogram,DCT,DFT,FFT|
|Image Conversion|Format Conversion-PNG,JPG,TIFF,BMP,WEBP|
|Tools|Background Removal,Sketches,HDR Effect|
|Exclusive|Object/Face/Edge Detection,Quality Enhancement|

---

## Requirements
See:

requirements.txt


