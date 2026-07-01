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
    
    return {"message": f"Image successfully processed for {conversionId}"}
    

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

    return {"message": f"Image successfully processed for {conversionId}"}


@app.post("/transformations")
async def iamge_transformation(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)

    if conversionId=='t6' or conversionId=='t7':
        if conversionId=='t6':
            width=int(image.shape[1]*2)
            height=int(image.shape[0]*2)
        else:
            width=int(image.shape[1]*0.5)
            height=int(image.shape[0]*0.5)

        upscale=cv2.resize(image,(width,height))
        cv2.imwrite('Scaled_image.jpg',upscale)
        return {"message": f"Image successfully processed for {conversionId}"}
        

    raise HTTPException(status_code=400, detail="Invalid detection ID")

@app.post("/detection")
async def image_detection(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    if conversionId=='d2':
        edge=cv2.Canny(image,100,200)
        cv2.imwrite('edges.jpg',edge)
        return {"message": f"Image successfully processed for {conversionId}"}
        
    raise HTTPException(status_code=400, detail="Invalid detection ID")


@app.post("/compress")
async def image_compression(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    intensity:int=Form(50)):
    image=await validate_image(file)
    if conversionId=='compress':
        #cv2.imwrite('compressed.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, compression_rate])
        cv2.imwrite('img.jpg',image,[cv2.IMWRITE_JPEG_QUALITY, intensity])
        

    
    

