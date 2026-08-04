# Eikona

Eikona is an image processing website that have different operations like Image Addition,Background removal,Object detection,etc.

It is build using React, FastAPI and OpenCV.

![Working](./frontend_eikona/Processing_Images/Demo.gif)
---
## Features
- Image Compression.
- Background Removal.
- Object Detection.
- User guide
- Multiple Output Formats.
---
## Installation
```bash
#clone Repository
git clone "https://github.com/muin-15/eikona.git"
cd eikona
```

Frontend
```bash
cd eikona/frontend_eikona

# Install dependencies
npm install

# Start developer server
npm run dev

#Build
npm run build

# Build preview
npm run preview

#Backend Connection
Update the backend url to use locally
```

Backend
```bash
cd eikona/backend_eikona

# Create Virtual Environment

#Windows
python -m venv venv
venv\Scripts\activate

#Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Running the server
uvicorn app.main:app --reload

# default url
http://127.0.0.1:8000

# Swagger documentation
http://127.0.0.1:8000/docs
```
---
## Project Structure
```
eikona/
├─ frontend_eikona/
│  ├─ index.html
│  ├─ src/
│  ├─ public/
│  └─ processing_images/
├─ backend_eikona/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models/
│  │  └─ yolo11n.pt
│  └─ .python-version
├─ Testing/
├─.gitignore
├─ .gitattributes
├─ LICENSE
└─ Readme.md
```

## Use of AI
- Ai tools are used to deploy the project and troubleshoot.

## LICENSE

[GPL 3.0 License](LICENSE)