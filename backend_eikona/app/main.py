from fastapi import FastAPI,UploadFile,File,Form #type:ignore
from fastapi.middleware.cors import CORSMiddleware #type:ignore
import cv2 #type:ignore
import numpy as np

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

image = cv2.imread('luffy.jpeg')

if image is None:
    print("Error: Could not read the image.")
    exit()

@app.post("/color_conversion")
async def convert_color(
    
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    contents=await file.read()
    nparr=np.frombuffer(contents,np.uint8)
    image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)

    if conversionId=="bgr1":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('luffy_gray.jpg', gray)
        return {"message": "Image converted to grayscale."}


"""
width_d = int(image.shape[1] *0.5)
height_d = int(image.shape[0] *0.5)
image_rd = cv2.resize(image, (width_d, height_d))
cv2.imshow('luffy_resizedDownscaled.jpg', image_rd)

width_d = int(image.shape[1] *2)
height_d = int(image.shape[0] *2)
image_ru = cv2.resize(image, (width_d, height_d))
cv2.imshow('luffy_resizedUpscaled.jpg', image_ru)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gaussian_filter = cv2.GaussianBlur(image, (5, 5), 0)
mean_filter=cv2.boxFilter(image, -1, (5, 5))
median_filter=cv2.medianBlur(image, 5)
laplacian_filter=cv2.Laplacian(image, cv2.CV_64F,ksize=3)
edges = cv2.Canny(gray, 100, 200)

cv2.imshow('edges.jpg', edges)
cv2.imshow('grayscale.jpg', gray)
cv2.imshow('gaussian_color.jpg', gaussian_filter)
cv2.imshow('mean_color.jpg', mean_filter)
cv2.imshow('median_color.jpg',median_filter)
cv2.imshow('Laplacian_color.jpg',laplacian_filter)

imggray2rgb=cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
imgbgr2hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
imghsv2bgr=cv2.cvtColor(imgbgr2hsv, cv2.COLOR_HSV2BGR)
imgbgr2rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
imgrgb2bgr=cv2.cvtColor(imgbgr2rgb, cv2.COLOR_RGB2BGR)


cv2.imshow('luffy_gray_to_rgb.jpg', imggray2rgb)
cv2.imshow('luffy_bgr_to_hsv.jpg', imgbgr2hsv)
cv2.imshow('luffy_hsv_to_bgr.jpg', imghsv2bgr)
cv2.imshow('luffy_bgr_to_rgb.jpg', imgbgr2rgb)
cv2.imshow('luffy_rgb_to_bgr.jpg', imgrgb2bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""