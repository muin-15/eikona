from fastapi import FastAPI,UploadFile,File,Form,HTTPException #type:ignore
from fastapi.middleware.cors import CORSMiddleware #type:ignore
import cv2 #type:ignore
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from rembg import remove
from typing import Optional

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

def psf_genretion(shape,length=20,angle=45):
    h,w=shape[:2]
    psf=np.zeros((h,w),dtype=np.float32)
    center=(h//2,w//2)
    cv2.line(psf,
            (center[0] - length // 2, center[1]), 
            (center[0] + length // 2, center[1]),
            1.0, 
            thickness=1)
    rotation_matrix=cv2.getRotationMatrix2D((center[0],center[1]),angle,1.0)
    psf=cv2.warpAffine(psf,rotation_matrix,(w,h))
    psf/=psf.sum()
    psf=np.fft.ifftshift(psf)
    return psf

def inverse_filter(image,psf_kernel,epsilon=1e-3):
    image=image.astype(np.float32)/255.0
    G=np.fft.fft2(image)
    H=np.fft.fft2(psf_kernel)
    H_safe=np.where(np.abs(H)<epsilon,epsilon,H)
    F=G/H_safe
    restored=np.real(np.fft.fft2(F))
    restored=np.clip(restored,0,1)

    return (restored*255).astype(np.uint8)

def wiener_filter(image,psf_kernel,k=0.01):
    image=image.astype(np.float32)/255.0
    G=np.fft.fft2(image)
    H=np.fft.fft2(psf_kernel)
    H_conj=np.conj(H)
    F=(H_conj/(np.abs(H) ** 2 +k))*G
    restored=np.real(np.fft.fft2(F))
    restored=np.clip(restored,0,1)

    return (restored*255).astype(np.uint8)

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
        raise HTTPException(status_code=404,detail="Please provide an Image")
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
    
    return {"message": "Image successfully processed"}
    

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

    elif conversionId=="filter5":
        bilateral=cv2.bilateralFilter(image,d=9,sigmaColor=75,sigmaSpace=75)
        cv2.imwrite('bilateral_blur.jpg',bilateral)

    return {"message": "Image successfully processed"}


@app.post("/transformations")
async def image_transformation(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    angle:Optional[float]=Form(None),
    gamma:Optional[float]=Form(None)):

    image=await validate_image(file)

    if conversionId=='t1' and angle:
        scale=1.0
        height,width=image.shape[:2]
        center=(width//2,height//2)
        rotation_matrix=cv2.getRotationMatrix2D(center,angle,scale)
        rotated_img=cv2.warpAffine(image,rotation_matrix,(width,height))
        cv2.imwrite('Rotated_img.jpg',rotated_img)
        return {"message":" Image rotated successfully"}

    elif conversionId=='t6' or conversionId=='t7':
        if conversionId=='t6':
            width=int(image.shape[1]*2)
            height=int(image.shape[0]*2)
        else:
            width=int(image.shape[1]*0.5)
            height=int(image.shape[0]*0.5)

        upscale=cv2.resize(image,(width,height))
        cv2.imwrite('Scaled_image.jpg',upscale)
        return {"message":"Image Scaled Successfully"}

    elif conversionId=='t2':
        bg_removed=remove(image)
        cv2.imwrite('Background_removed.jpg',bg_removed)
        return {"message": "Image successfully processed"}
    
    elif conversionId=='t3':
        negative_img=255-image
        cv2.imwrite('Negative_img.jpg',negative_img)
        return {"message":"Negative Transformation Applied Successfully"}
    
    elif conversionId=='t4':
        if gamma>=0 and gamma<=5:
            table=np.array([((i/255)**gamma)*255 for i in np.arange(0,256)]).astype("uint8")
            power_law=cv2.LUT(image,table)
            cv2.imwrite('Power_law_img.jpg',power_law)
            return {"message":"PowerLaw Transformation Applied Successfully"}
        else:
            raise HTTPException(status_code=400,detail="Provide Gamma Value between 0.1-5.0")

    elif conversionId=='t5':
        img_float=image.astype(np.float32)
        max_val=np.max(img_float)
        c=255/np.log(1+max_val) if max_val> 0 else 1
        log_img=c*np.log(1+img_float)
        restored_log=cv2.convertScaleAbs(log_img)
        cv2.imwrite('Log_img.jpg',restored_log)
        return {"message":"Log Transformation Applied Successfully"}

    raise HTTPException(status_code=400, detail="Invalid detection ID")

@app.post("/detection")
async def image_detection(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    if conversionId=='d1':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret,thresh=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        cv2.imwrite('threshold_img(binary).jpg',thresh)
        return {"message":"Transformed to binary successfully"}
    elif conversionId=='d2':
        edge=cv2.Canny(image,100,200)
        cv2.imwrite('edges.jpg',edge)
        return {"message": "Image successfully processed"}
        
    raise HTTPException(status_code=400, detail="Invalid detection ID")


@app.post("/compress")
async def image_compression(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    intensity:int=Form(50)):
    image=await validate_image(file)
    if conversionId=='compress':
        
        cv2.imwrite('img.jpg',image,[cv2.IMWRITE_JPEG_QUALITY, intensity])
        return{"message": f"Image successfully compressed with intensity {intensity}"}
    raise HTTPException(status_code=400, detail="Invalid compression ID")

@app.post("/operations")
async def image_operations(
    file:UploadFile=File(...),
    file2:UploadFile=File(...),
    conversionId:str=Form(...)):
    image1=await validate_image(file)
    image2=await validate_image(file2)

    if conversionId=='add':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400, detail="Images must have the same dimensions for addition")
        added=cv2.add(image1,image2)
        cv2.imwrite('added_img.jpg',added)
        return {"message": "Images Successfully added"}
    
    elif conversionId=='sub':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for subtraction")
        subtract=cv2.subtract(image1,image2)
        cv2.imwrite('subtracted_img.jpg',subtract)
        return {"message":"Images Successfully subtracted"}
    
    elif conversionId=='mul':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for multiplication")
        multiplied=cv2.multiply(image1,image2)
        cv2.imwrite('multiplied_img.jpg',multiplied)
        return {"message":"Images Successfully multiplicated"}
    
    elif conversionId=='div':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for division")
        divided=cv2.divide(image1,image2)
        cv2.imwrite('divided_img.jpg',divided)
        return {"message":"Images Successfully divided"}
    raise HTTPException(status_code=400, detail="Invalid operation ID")

@app.post("/analytics")
async def image_analytics(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file) 
    colors=('b','g','r')

    if conversionId=='histogram': 
        fig=Figure(figsize=(7,4))
        ax = fig.subplots() 
        ax.set_title('Histogram Analysis')
        ax.set_xlabel('Pixel Value')
        ax.set_ylabel('Frequency')
        for i,color in enumerate(colors):
            img_hist=cv2.calcHist([image],[i],None,[256],[0,256])
            ax.plot(img_hist,color=color,label=f'{color.upper()} Channel')
        
        ax.set_xlim([0,256])
        ax.legend()
        ax.grid(True)
        fig.savefig('img_hist.png',bbox_inches='tight')
        return {"message": "Image successfully processed"}
    
    elif conversionId=='dft':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dft_img=cv2.dft(np.float32(image),flags=cv2.DFT_COMPLEX_OUTPUT) 
        magnitude_spectrum=20*np.log(cv2.magnitude(dft_img[:,:,0],dft_img[:,:,1]))
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(magnitude_spectrum,cmap='gray')
        fig.savefig('img_dft.png',bbox_inches='tight')
        return {"message": "Image successfully processed"}
    
    elif conversionId=='dct':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dct_img=cv2.dct(np.float32(image))
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(dct_img,cmap='gray')
        fig.savefig('img_dct.png',bbox_inches='tight')
        return {"message": "Image successfully processed"}
    
    elif conversionId=='fft':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        f=np.fft.fft2(image)
        fshift=np.fft.fftshift(f)
        magnitude_spectrum=20*np.log(np.abs(fshift))
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(magnitude_spectrum,cmap='gray')
        fig.savefig('img_fft.png',bbox_inches='tight')
        return {"message": "Image successfully processed"}
    return("Analysis Done Successfully")

@app.post('/image_conversion')
async def image_conversions(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)
    
    if conversionId=='topng':
        cv2.imwrite('png_converted.png',image)
        return {"message":"Converted to PNG"}
    
    elif conversionId=='tojpg':
        cv2.imwrite('jpg_converted.jpg',image)
        return {"message":"Converted to JPG"}
    
    elif conversionId=='tobmp':
        cv2.imwrite('bmp_converted.bmp',image)
        return {"message":"Converted to BMP"}
    
    elif conversionId=='totiff':
        cv2.imwrite('tiff_converted.tiff',image)
        return {"message":"Converted to TIFF"}
    
    elif conversionId=='towebp':
        cv2.imwrite('webp_converted.webp',image)
        return {"message":"Converted to WEBP"}
    
    raise HTTPException(status_code=400,detail="Invalide extension for operation")

@app.post('/restoration')
async def Image_restoration(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    if len(image.shape)==3:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    psf=psf_genretion(image.shape,length=25,angle=30)

    if conversionId=='res1':
        restored=inverse_filter(image,psf)
    elif conversionId=='res2':
        restored=wiener_filter(image,psf,k=0.01)
    else: 
        raise HTTPException(status_code=400,detail='Invalid processing')
    cv2.imwrite('restored.png',restored)
    return {"message":"Image Restored Successfully"}

@app.post('/tools')
async def image_tools(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    sigmaS:Optional[float]=Form(None),
    sigmaR:Optional[float]=Form(None)):

    image=await validate_image(file)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    if conversionId=='tool1':
        bg_remove=remove(image)
        cv2.imwrite('Background_removed.jpg',bg_remove)
        return {"message":"Background Removed Successfully"}
    
    elif conversionId=='tool2' and (sigmaS or sigmaR):
        style_image=cv2.stylization(image,sigma_s=sigmaS,sigma_r=sigmaR)
        cv2.imwrite('stilyzed_img.jpg',style_image)
        return {"message":"Image Stylized Properly"}
    
    elif conversionId=='tool3':
        enhance=cv2.inpaint(image,mask,3,cv2.INPAINT_TELEA)
        cv2.imwrite('Enhanced_img.jpg',enhance)
        return {"message":"Image Enhanced Successfully"}
    
    elif conversionId=='tool4' and (sigmaS or sigmaR):
        gray,pencil_img=cv2.pencilSketch(image,sigma_s=sigmaS,sigma_r=sigmaR,shade_factor=0.05)
        cv2.imwrite("pencil_sketch.jpg",pencil_img)
        return {"message":"Image Enhanced Successfully"}
    
    elif conversionId=='tool5' and (sigmaS or sigmaR):
        hdr_img=cv2.detailEnhance(image,sigma_s=sigmaS,sigma_r=sigmaR)
        cv2.imwrite('hdr_img.jpg',hdr_img)
        return {"message":"Image Enhanced Successfully"}
    
    raise HTTPException(status_code=400,detail='Provide Image for Background Removal')