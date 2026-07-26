# EIKONA

Eikona is an Image-processing tool that contains more than 35 tools which are based on different perspectives.

Eikona is easy,simple and powerful Image processing tool.It's designed for beginners and experts that are learning and Adapting to Image processing.

![Work Process](./frontend_eikona/Processing_Images/Demo.gif)

---
## Features
- 35+ different Image processing tools.
- Demanding tools like Background Removal and Image compression.
- Preview of Resultant Image and Downloadable in different formats.
- User-guide and Support provided.
- Individual path for each operation.

---
## Installation
```bash
# Clone Repo
git clone "https://github.com/muin-15/eikona.git"
cd eikona
```

Frontend
```bash
cd eikona/frontend_eikona

# Install dependencies
npm install

# Start development Server
npm run dev

# Build
npm run build

# Build preview
npm run preview

# Backend connection
Update the Backend url to use locally
```

Backend
```bash
cd eikona/backend_eikona

# Create Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Running the server
uvicorn app.main:app --reload

# default url
http://127.0.0.1:8000

# Swagger Documentation
http://127.0.0.1:8000/docs

```

---
## Project Structure
```
eikona/
├── Testing/
│
├── backend_eikona/
│   ├─ app/
│   │  ├─ main.py
│   │  ├─ models/
│   │  └─ yolo11n.pt
│   └─ .python-version
│   
├── frontend_eikona/
│   ├─ index.html
│   ├─ src/
│   │  ├─ assets
│   │  ├─ index.css
│   │  ├─ App.tsx
│   │  ├─ main.tsx
│   │  └─ App.css
│   ├─ public/
│   │  ├─ user-guide.html
│   │  └─ userguide.css
│   └─ Processing_Images
│   
├─ .gitignore
├─ .gitattributes
├─ LICENSE
└─ Readme.md
```

---
## License

The project is under the [GPL 3.0 License](LICENSE)
