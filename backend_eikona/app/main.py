from fastapi import FastAPI,UploadFile,File,Form,HTTPException #type:ignore
from fastapi.middleware.cors import CORSMiddleware #type:ignore
import cv2 #type:ignore
import numpy as np
import uuid


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

async def validate_image(file:UploadFile):
    contents=await file.read()
    nparr=np.frombuffer(contents,np.uint8)

    if len(nparr)==0:
        print("Error Image van't be loaded")
        raise HTTPException(status_code=404,detail="Image not present")

    image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)

    if image is None:
        return("can't process")
        raise HTTPException(statue_code=404,detail="Please provide an Image")
    return image


@app.post("/color_conversion")
async def convert_color(
    
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)

    if conversionId=="bgr1":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('bgr_gray.jpg', gray)
        return {"message": "Image converted to grayscale."}
    elif conversionId=="bgr2":
        if image.ndim == 3 and image.shape[2] == 3:
           color=cv2.applyColorMap(image,cv2.COLORMAP_TWILIGHT_SHIFTED)
        elif image.ndim==1:
            color=cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        
        cv2.imwrite('gray_bgr.jpg',color)
        
    elif conversionId=="bgr3":
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
        cv2.imwrite('bgr_hsv.jpg',hsv)

    elif conversionId=="bgr4":
        hsv_bgr=cv2.cvtColor(image,cv2.COLOR_HSV2BGR)
        cv2.imwrite('hsv_bgr.jpg',hsv_bgr)

    elif conversionId=="bgr5":
        rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        cv2.imwrite('bgr_rgb.jpg',rgb)

    elif conversionId=="bgr6":
        rgb_bgr=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imwrite('rgb_bgr.jpg',rgb_bgr)

    else:
        return("404 Error can't proceed")
    

@app.post("/filtering")
async def image_filter(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)

    if conversionId=="filter3":
        gaussian=cv2.GaussianBlur(image,(5,5),0)
        cv2.imwrite('gaussian_blur.jpg',gaussian)

    elif conversionId=="filter1":
        mean=cv2.boxFilter(image,-1,(5,5))
        cv2.imwrite('mean_blur.jpg',mean)

    elif conversionId=="filter2":
        median=cv2.medianBlur(image,5)
        cv2.imwrite('median_blur.jpg',median)

    elif conversionId=="filter4":
        laplacian=cv2.Laplacian(image,cv2.CV_64F,ksize=3)
        cv2.imwrite('laplacian_blur.jpg',laplacian)

"""
width_d = int(image.shape[1] *0.5)
height_d = int(image.shape[0] *0.5)
image_rd = cv2.resize(image, (width_d, height_d))
cv2.imshow('luffy_resizedDownscaled.jpg', image_rd)
 
width_d = int(image.shape[1] *2)
height_d = int(image.shape[0] *2)
image_ru = cv2.resize(image, (width_d, height_d))
cv2.imshow('luffy_resizedUpscaled.jpg', image_ru)

gaussian_filter = cv2.GaussianBlur(image, (5, 5), 0)
mean_filter=cv2.boxFilter(image, -1, (5, 5))
median_filter=cv2.medianBlur(image, 5)
laplacian_filter=cv2.Laplacian(image, cv2.CV_64F,ksize=3)
edges = cv2.Canny(gray, 100, 200)

cv2.imshow('edges.jpg', edges)
cv2.imshow('gaussian_color.jpg', gaussian_filter)
cv2.imshow('mean_color.jpg', mean_filter)
cv2.imshow('median_color.jpg',median_filter)
cv2.imshow('Laplacian_color.jpg',laplacian_filter)

imghsv2bgr=cv2.cvtColor(imgbgr2hsv, cv2.COLOR_HSV2BGR)
imgbgr2rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
imgrgb2bgr=cv2.cvtColor(imgbgr2rgb, cv2.COLOR_RGB2BGR)

cv2.imshow('luffy_hsv_to_bgr.jpg', imghsv2bgr)
cv2.imshow('luffy_bgr_to_rgb.jpg', imgbgr2rgb)
cv2.imshow('luffy_rgb_to_bgr.jpg', imgrgb2bgr)
"""
cv2.waitKey(0)
cv2.destroyAllWindows()