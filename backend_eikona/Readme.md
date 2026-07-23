# ⚙️EIKONA Backend

> High Performance FastAPI backend powering Eikona an image processing tool.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)
![GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)

---

## 📖 Overview

The Eikona Backend provides RestAPI for image processing using FastAPI.It handles image uploading ,validation ,processing and returns the image with user specified format to the Frontend.

The Spotlights for the backend are AI algorithms like YuNet and YOLO.
Backend combines the traditional search and computer vision for Image processing.

---

## ✨ Features

- 📉Image Compression
- 🪬Image Combining & Operations
- 🎨Color Conversion
- 🎯Transformations
- 🎞️Filtering
- 🛠️Restoration
- 📊Analytics
- 🤖Background Removal
- ✏️Pencil Sketch
- 🕵️YuNet:Face Detection
- 🥨Image Format Conversion
- 🚞AI based Processing
- 🌟CLAHE Enhacement

---

## ⚙️ Tech Stack

- FastAPI
- Python 
- Ultralytics YOLO
- YuNet
- rembg
- Pillow
- Uvicorn
- NumPy
- OpenCV

---

## 📂 Project Structure

```
backend_eikona/
├── .python-version
├── app/
│   ├── dependencies.py
│   ├── main.py
│   ├── models/
│   │   └── face_detection_yunet_2023mar.onnx
│   └── yolo11n.pt
├── requirements.txt
└── runtime.txt
```

---

## 🚀 Installation

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

## ▶️ Running the Server
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

## 📌 API Modules

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

## 📄 Requirements
See:

requirements.txt

---

## 📜 License

This backend is part of the Eikona project and is licensed under the GNU General Public License v3.0 (GPL-3.0).

See the root LICENSE file for complete license terms.

