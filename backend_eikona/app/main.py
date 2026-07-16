from fastapi import FastAPI,UploadFile,File,Form,HTTPException #type:ignore
from fastapi.middleware.cors import CORSMiddleware #type:ignore
from fastapi.responses import Response
import cv2 #type:ignore
import numpy as np #type:ignore
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from rembg import remove #type:ignore
from typing import Optional
import io

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

def psf_genretion(shape,cid,length=20,angle=45):
    h,w=shape[:2]
    psf=np.zeros((h,w),dtype=np.float32)
    center=(w//2,h//2)
    cv2.line(psf,
            (center[0] - length // 2, center[1]), 
            (center[0] + length // 2, center[1]),
            1.0, 
            thickness=1)
    rotation_matrix=cv2.getRotationMatrix2D((center),angle,1.0)
    psf=cv2.warpAffine(psf,rotation_matrix,(w,h))
    psf/=psf.sum()
    return psf
   

def inverse_filter(image,psf_kernel,epsilon=1e-3):
    image=image.astype(np.float32)/255.0
    G=np.fft.fft2(image)
    H=np.fft.fft2(psf_kernel)
    H_safe=np.where(np.abs(H)<epsilon,epsilon,H)
    F=G/H_safe
    restored=np.real(np.fft.ifft2(F))
    restored=np.clip(restored,0,1)

    return (restored*255).astype(np.uint8)

def wiener_filter(image,psf_kernel,k=0.01):
    image=image.astype(np.float32)/255.0
    G=np.fft.fft2(image)
    H=np.fft.fft2(psf_kernel)
    H_conj=np.conj(H)
    F=(H_conj/(np.abs(H) ** 2 +k))*G
    restored=np.real(np.fft.ifft2(F))
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
        success, encoded_image = cv2.imencode('.jpg', gray)
        
    elif conversionId=='d1':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret,thresh=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        success,encoded_image=cv2.imencode('.jpg',thresh)
        
        
    elif conversionId=="bgr3":
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
        success,encoded_image=cv2.imencode('.jpg',hsv)

    elif conversionId=="bgr4":
        hsv_bgr=cv2.cvtColor(image,cv2.COLOR_HSV2BGR)
        success,encoded_image=cv2.imencode('.jpg',hsv_bgr)

    elif conversionId=="bgr5":
        rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        success,encoded_image=cv2.imencode('.jpg',rgb)

    elif conversionId=="bgr6":
        rgb_bgr=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        success,encoded_image=cv2.imencode('.jpg',rgb_bgr)

    elif conversionId=="bgr7":
        bgr_lab=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
        success,encoded_image=cv2.imencode('.jpg',bgr_lab)

    elif conversionId=='bgr8':
        lab_bgr=cv2.cvtColor(image,cv2.COLOR_LAB2BGR)
        success,encoded_image=cv2.imencode('.jpg',lab_bgr)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown conversionId: {conversionId}")

    if not success:
            return ("404 can't process image")

    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')
    
    
    

@app.post("/filtering")
async def image_filter(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)

    if conversionId=="filter3":
        gaussian=cv2.GaussianBlur(image,(5,5),0)
        success,encoded_image=cv2.imencode('.jpg',gaussian)

    elif conversionId=="filter1":
        mean=cv2.boxFilter(image,-1,(5,5))
        success,encoded_image=cv2.imencode('.jpg',mean)

    elif conversionId=="filter2":
        median=cv2.medianBlur(image,5)
        success,encoded_image=cv2.imencode('.jpg',median)

    elif conversionId=="filter4":
        laplacian=cv2.Laplacian(image,cv2.CV_64F,ksize=3)
        success,encoded_image=cv2.imencode('.jpg',laplacian)

    elif conversionId=="filter5":
        bilateral=cv2.bilateralFilter(image,d=9,sigmaColor=75,sigmaSpace=75)
        success,encoded_image=cv2.imencode('.jpg',bilateral)

    else:
        return {"message": "Invalid conversionId"}

    if not success:
        return ("Can't process image")
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')



@app.post("/transformations")
async def image_transformation(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    angle:Optional[float]=Form(None),
    gamma:Optional[float]=Form(None)):

    image=await validate_image(file)

    if conversionId=='t1' and angle is not None:
        scale=1.0
        height,width=image.shape[:2]
        center=(width//2,height//2)
        rotation_matrix=cv2.getRotationMatrix2D(center,angle,scale)
        rotated_img=cv2.warpAffine(image,rotation_matrix,(width,height))
        success,encoded_image=cv2.imencode('.jpg',rotated_img)


    elif conversionId=='t6' or conversionId=='t7':
        if conversionId=='t6':
            width=int(image.shape[1]*2)
            height=int(image.shape[0]*2)
        else:
            width=int(image.shape[1]*0.5)
            height=int(image.shape[0]*0.5)

        upscale=cv2.resize(image,(width,height))
        success,encoded_image=cv2.imencode('.jpg',upscale)

    elif conversionId=='t2':
        bg_removed=remove(image)
        success,encoded_image=cv2.imencode('.jpg',bg_removed)
    
    elif conversionId=='t3':
        negative_img=255-image
        
        success,encoded_image=cv2.imencode('.jpg',negative_img)
    
    elif conversionId=='t4':
        if gamma>=0 and gamma<=5:
            table=np.array([((i/255)**gamma)*255 for i in np.arange(0,256)]).astype("uint8")
            power_law=cv2.LUT(image,table)
            success,encoded_image=cv2.imencode('.jpg',power_law)
        else:
            raise HTTPException(status_code=400,detail="Provide Gamma Value between 0.1-5.0")

    elif conversionId=='t5':
        img_float=image.astype(np.float32)
        max_val=np.max(img_float)
        c=255/np.log(1+max_val) if max_val> 0 else 1
        log_img=c*np.log(1+img_float)
        restored_log=cv2.convertScaleAbs(log_img)
        success,encoded_image=cv2.imencode('.jpg',restored_log)

    else:
        raise HTTPException(status_code=400, detail="Invalid detection ID")
    
    if not success:
        return ("404 can't process image")
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')

@app.post("/detection")
async def image_detection(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    
    if conversionId=='d2':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edge=cv2.Canny(gray,100,200)
        success,encoded_image=cv2.imencode('.jpg',edge)
        
    else:
        raise HTTPException(status_code=400, detail="Invalid detection ID")
    
    if not success:
        return ("404: can't process image")
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')


@app.post("/compress")
async def image_compression(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    intensity:int=Form(50)):
    image=await validate_image(file)
    if conversionId=='compress':
        
        sucess,encoded_image=cv2.imencode('.jpg',image,[cv2.IMWRITE_JPEG_QUALITY, intensity])
        if not sucess:
            return ("404: Can't process image")
        return Response(content=encoded_image.tobytes(),media_type='image/jpeg')
    else:
        raise HTTPException(status_code=404,detail="Inavlid conversionId")

    

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
        success,encoded_image=cv2.imencode('.jpg',added)

    
    elif conversionId=='sub':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for subtraction")
        subtract=cv2.subtract(image1,image2)
        success,encoded_image=cv2.imencode('.jpg',subtract)
    
    elif conversionId=='mul':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for multiplication")
        multiplied=cv2.multiply(image1,image2)
        success,encoded_image=cv2.imencode('.jpg',multiplied)
    
    elif conversionId=='div':
        if image1.shape!=image2.shape:
            raise HTTPException(status_code=400,detail="Images must have the same dimensions for division")
        divided=cv2.divide(image1,image2)
        success,encoded_image=cv2.imencode('.jpg',divided)

    else:
        raise HTTPException(status_code=400, detail="Invalid operation ID")
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')

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
        if image.ndim==2:
            hist=cv2.calcHist([image],[0],None,[256],[0,256])
            ax.plot(hist,color='black',label='Intensity')
        else:
            for i,color in enumerate(colors):
                hist=cv2.calcHist([image],[i],None,[256],[0,256])
                ax.plot(hist,color=color,label=f'{color.upper()} channel')

        ax.set_xlim([0,256])
        ax.legend()
        ax.grid(True)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return Response(content=buf.getvalue(),media_type='image/png')

    
    elif conversionId=='dft':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dft_img=cv2.dft(np.float32(image),flags=cv2.DFT_COMPLEX_OUTPUT) 
        dft_shift=np.fft.fftshift(dft_img)
        magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(magnitude_spectrum,cmap='gray')
        ax.set_title("DFT Transformation")
        ax.axis('off')

        buf= io.BytesIO()
        fig.savefig(buf,format='png',bbox_inches='tight')
        buf.seek(0)
        return Response(content=buf.getvalue(),media_type='image/png')
    
    elif conversionId=='dct':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = image.shape
        image_f = np.float32(image)
        if h % 2 != 0:
            image_f = image_f[:-1, :]
        if w % 2 != 0:
            image_f = image_f[:, :-1]

        dct_img = cv2.dct(image_f)
        dct_log = np.log(np.abs(dct_img) + 1e-8)
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(dct_log,cmap='gray')
        ax.set_title("DCT Transformation")
        ax.axis('off')

        buf=io.BytesIO()
        fig.savefig(buf,format='png',bbox_inches='tight')
        buf.seek(0)
        return Response(content=buf.getvalue(),media_type='image/png')
        
        
    
    elif conversionId=='fft':
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        f=np.fft.fft2(image)
        fshift=np.fft.fftshift(f)
        magnitude_spectrum=20*np.log(np.abs(fshift))
        fig=Figure(figsize=(7,4))
        ax=fig.add_subplot(1,1,1)
        ax.imshow(magnitude_spectrum,cmap='gray')
        ax.set_title('FFt Transformation')
        ax.axis('off')
        
        buf=io.BytesIO()
        fig.savefig(buf,format='png',bbox_inches='tight')
        buf.seek(0)
        return Response(content=buf.getvalue(),media_type='image/png')

        
    
    else:
        raise HTTPException(status_code=400,detail="Can't process successfully")

@app.post('/image_conversion')
async def image_conversions(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):

    image=await validate_image(file)
    
    if conversionId=='toconvert':
        success,encoded_image=cv2.imencode('.png',image)
        if not success:
            return ('Invalid Format')
        return Response(content=encoded_image.tobytes(),media_type='image/png')
    
    else:
        raise HTTPException(status_code=400,detail="Invalide extension for operation")

@app.post('/restoration')
async def Image_restoration(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    cid=conversionId
    if len(image.shape)==3:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    psf=psf_genretion(image.shape,cid,length=25,angle=30,)

    if conversionId=='res1':
        restored=inverse_filter(image,psf)
    elif conversionId=='res2':
        restored=wiener_filter(image,psf,k=0.01)
    else: 
        raise HTTPException(status_code=400,detail='Invalid processing')
    success,encoded_image=cv2.imencode('.jpg',restored)
    if not success:
        return ('500 : server Error')
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')

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
        success,encoded_image=cv2.imencode('.jpg',bg_remove)
    
    elif conversionId=='tool2' and (sigmaS or sigmaR):
        style_image=cv2.stylization(image,sigma_s=sigmaS,sigma_r=sigmaR)
        success,encoded_image=cv2.imencode('.jpg',style_image)
    
    elif conversionId=='tool3':
        enhance=cv2.inpaint(image,mask,3,cv2.INPAINT_TELEA)
        success,encoded_image=cv2.imencode('.jpg',enhance)
    
    elif conversionId=='tool4' and (sigmaS or sigmaR):
        gray,pencil_img=cv2.pencilSketch(image,sigma_s=sigmaS,sigma_r=sigmaR,shade_factor=0.05)
        success,encoded_image=cv2.imencode('.jpg',pencil_img)
    
    elif conversionId=='tool5' and (sigmaS or sigmaR):
        hdr_img=cv2.detailEnhance(image,sigma_s=sigmaS,sigma_r=sigmaR)
        success,encoded_image=cv2.imencode('.jpg',hdr_img)
    
    else:
        raise HTTPException(status_code=400,detail='Invalid conversionId')
    if not success:
        return ("500 Can't process Image")
    
    return Response(content=encoded_image.tobytes(),media_type='image/jpeg')