from fastapi import FastAPI,UploadFile,File,Form,HTTPException #type:ignore
from fastapi.middleware.cors import CORSMiddleware #type:ignore
from fastapi.responses import Response #type:ignore
import cv2 #type:ignore
import numpy as np #type:ignore
import matplotlib.pyplot as plt #type:ignore
from matplotlib.figure import Figure    #type:ignore
from typing import Optional
import io
import os
import json #type:ignore

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://eikona-img-khaki.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Objects-Counts"]
)

modelpath=os.path.join(
    os.path.dirname(__file__),
    "models",
    "face_detection_yunet_2023mar.onnx"
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

_yolo_model = None
def get_yolo_model():
    global _yolo_model
    if _yolo_model is None:
        from ultralytics import YOLO #type:ignore
        _yolo_model = YOLO("yolo11n.pt")
    return _yolo_model

def encoded_image_gen(image,output_Format=".jpg"):
    fmt=output_Format.lower()
    if fmt=='jpg':
        ext,mime=".jpg","image/jpeg"
    elif fmt=='png':
        ext,mime='.png','image/png'
    elif fmt=='bmp':
        ext,mime='.bmp','image/bmp'
    elif fmt in ('tif','tiff'):
        ext,mime='.tiff','image/tiff'
    elif fmt=='webp':
        ext,mime='.webp','image/webp'
    else:
        raise HTTPException(status_code=400,detail="Invalid Format")
    success,encoded_image=cv2.imencode(ext,image)

    if not success:
        raise HTTPException(status_code=500,detail="Server Error")
    return Response(content=encoded_image.tobytes(),media_type=mime)


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
    conversionId:str=Form(...),
    outputFormat:Optional[str]=Form(...)):

    image=await validate_image(file)

    if conversionId=="bgr1":
        g = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    elif conversionId=='d1':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret,g=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        
    elif conversionId=="bgr3":
        g=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 

    elif conversionId=="bgr4":
        g=cv2.cvtColor(image,cv2.COLOR_HSV2BGR)

    elif conversionId=="bgr5":
        g=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    elif conversionId=="bgr6":
        g=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    elif conversionId=="bgr7":
        g=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

    elif conversionId=='bgr8':
        g=cv2.cvtColor(image,cv2.COLOR_LAB2BGR)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown conversionId: {conversionId}")
    
    return encoded_image_gen(g,outputFormat)


    

@app.post("/filtering")
async def image_filter(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    outputFormat:Optional[str]=Form(...)):

    image=await validate_image(file)

    if conversionId=="filter3":
        filtered=cv2.GaussianBlur(image,(5,5),0)

    elif conversionId=="filter1":
        filtered=cv2.boxFilter(image,-1,(5,5))

    elif conversionId=="filter2":
        filtered=cv2.medianBlur(image,5)

    elif conversionId=="filter4":
        laplacian=cv2.Laplacian(image,cv2.CV_64F,ksize=3)
        filtered=cv2.convertScaleAbs(laplacian)

    elif conversionId=="filter5":
        filtered=cv2.bilateralFilter(image,d=9,sigmaColor=75,sigmaSpace=75)

    else:
        return {"message": "Invalid conversionId"}

    return encoded_image_gen(filtered,outputFormat)


@app.post("/transformations")
async def image_transformation(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    angle:Optional[float]=Form(None),
    gamma:Optional[float]=Form(None),
    outputFormat:Optional[str]=Form(...)):

    image=await validate_image(file)

    if conversionId=='t1' and angle is not None:
        scale=1.0
        height,width=image.shape[:2]
        center=(width//2,height//2)
        rotation_matrix=cv2.getRotationMatrix2D(center,angle,scale)
        transformed=cv2.warpAffine(image,rotation_matrix,(width,height))


    elif conversionId=='t6' or conversionId=='t7':
        if conversionId=='t6':
            width=int(image.shape[1]*2)
            height=int(image.shape[0]*2)
        else:
            width=int(image.shape[1]*0.5)
            height=int(image.shape[0]*0.5)

        transformed=cv2.resize(image,(width,height))

    
    elif conversionId=='t3':

        transformed=255-image
    
    elif conversionId=='t4':
        if gamma>=0 and gamma<=5:
            table=np.array([((i/255)**gamma)*255 for i in np.arange(0,256)]).astype("uint8")
            transformed=cv2.LUT(image,table)

        else:
            raise HTTPException(status_code=400,detail="Provide Gamma Value between 0.1-5.0")

    elif conversionId=='t5':
        img_float=image.astype(np.float32)
        max_val=np.max(img_float)
        c=255/np.log(1+max_val) if max_val> 0 else 1
        log_img=c*np.log(1+img_float)
        transformed=cv2.convertScaleAbs(log_img)

    else:
        raise HTTPException(status_code=400, detail="Invalid detection ID")
    
    return encoded_image_gen(transformed,outputFormat)


@app.post("/compress")
async def image_compression(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    intensity:int=Form(50),
    outputFormat:Optional[str]=Form(...)):
    image=await validate_image(file)
    if conversionId=='compress':
        
        success,encoded_image=cv2.imencode('.jpg',image,[cv2.IMWRITE_JPEG_QUALITY, intensity])
        if not success:
            raise HTTPException(status_code=500,detail="Internal Error")
        return Response(content=encoded_image.tobytes(),media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404,detail="Inavlid conversionId")

    

@app.post("/operations")
async def image_operations(
    file:UploadFile=File(...),
    file2:UploadFile=File(...),
    conversionId:str=Form(...),
    outputFormat:Optional[str]=Form(...)):

    image1=await validate_image(file)
    image2=await validate_image(file2)
    
    if image1.shape != image2.shape:
        h1,w1=image1.shape[:2]
        image2new=cv2.resize(image2,(w1,h1))

    else:
        image2new=image2.copy()

    if conversionId=='add':
        
        operation=cv2.add(image1,image2new)
    
    elif conversionId=='sub':
        
        operation=cv2.subtract(image1,image2new)
    
    elif conversionId=='mul':
        
        operation=cv2.multiply(image1,image2new)
    
    elif conversionId=='div':
        
        operation=cv2.divide(image1,image2new)

    else:
        raise HTTPException(status_code=400, detail="Invalid operation ID")
    return encoded_image_gen(operation,outputFormat)

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
        plt.close(fig)
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
        plt.close(fig)
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
        plt.close(fig)
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
        plt.close(fig)
        return Response(content=buf.getvalue(),media_type='image/png')


    else:
        raise HTTPException(status_code=400,detail="Can't process successfully")

@app.post('/image_conversion')
async def image_conversions(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    outputFormat:Optional[str]=Form(...)):

    image=await validate_image(file)
    
    if conversionId=='toconvert':
        return encoded_image_gen(image,outputFormat)

    else:
        raise HTTPException(status_code=400,detail="Invalide extension for operation")

@app.post('/restoration')
async def Image_restoration(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    angle:Optional[float]=Form(45.0),
    length:Optional[int]=Form(25),
    outputFormat:Optional[str]=Form(...)):
    image=await validate_image(file)
    cid=conversionId
    if len(image.shape)==3:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    psf=psf_genretion(image.shape,cid,length=length,angle=angle)

    if conversionId=='res1':
        restored=inverse_filter(image,psf)
    elif conversionId=='res2':
        restored=wiener_filter(image,psf,k=0.01)
    else: 
        raise HTTPException(status_code=400,detail='Invalid processing')
    
    return encoded_image_gen(restored,outputFormat)

@app.post('/tools')
async def image_tools(
    file:UploadFile=File(...),
    conversionId:str=Form(...),
    sigmaS:Optional[float]=Form(None),
    sigmaR:Optional[float]=Form(None)):

    image=await validate_image(file)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    if conversionId=='tool1':
        from rembg import remove #type:ignore
        bg_remove=remove(image)
        success,encoded_image=cv2.imencode('.png',bg_remove)
    
    elif conversionId=='tool2' and (sigmaS or sigmaR):
        style_image=cv2.stylization(image,sigma_s=sigmaS,sigma_r=sigmaR)
        success,encoded_image=cv2.imencode('.png',style_image)
    
    elif conversionId=='tool3':
        kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

        blackhat=cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT,kernel)
        _,mask=cv2.threshold(blackhat,10,255,cv2.THRESH_BINARY)

        enhance=cv2.inpaint(image,mask,3,cv2.INPAINT_TELEA)
        success,encoded_image=cv2.imencode('.png',enhance)

    elif conversionId=='tool4' and (sigmaS or sigmaR):
        gray,pencil_img=cv2.pencilSketch(image,sigma_s=sigmaS,sigma_r=sigmaR,shade_factor=0.05)
        success,encoded_image=cv2.imencode('.png',pencil_img)
    
    elif conversionId=='tool5' and (sigmaS or sigmaR):
        hdr_img=cv2.detailEnhance(image,sigma_s=sigmaS,sigma_r=sigmaR)
        success,encoded_image=cv2.imencode('.png',hdr_img)
    
    else:
        raise HTTPException(status_code=400,detail='Invalid conversionId')
    if not success:
        return ("500 Can't process Image")
    
    return Response(content=encoded_image.tobytes(),media_type='image/png')

@app.post('/exclusive')
async def highend_tools(
    file:UploadFile=File(...),
    conversionId:str=Form(...)):
    image=await validate_image(file)
    headers={}
    if conversionId=='e1':
        lab=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
        channel_l,channel_a,channel_b=cv2.split(lab)
        CLAHE=cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8,8))
        cl=CLAHE.apply(channel_l)
        mergedlab=cv2.merge((cl,channel_a,channel_b))
        enhanced_img=cv2.cvtColor(mergedlab,cv2.COLOR_LAB2BGR)
        final_ouput=cv2.bilateralFilter(enhanced_img,d=9,sigmaColor=75,sigmaSpace=75)
        success,encoded_img=cv2.imencode('.png',final_ouput)

    elif conversionId=='e2':
        detector=cv2.FaceDetectorYN.create(
            model=modelpath,
            config="",
            input_size=(320,320),
            score_threshold=0.8,
            nms_threshold=0.3,
            top_k=5000
        )
        h,w=image.shape[:2]
        detector.setInputSize((w,h))

        _,faces=detector.detect(image)
        if faces is None:
            return ("Image doesn't contain any faces")
        
        for i,face in enumerate(faces,start=1):
            x,y,fw,fh=face[:4].astype(int)
            confidence=face[-1]
            cv2.rectangle(
                image,
                (x,y),
                (x+fw,y+fh),
                (0,255,0),
                2
            )
            cv2.putText(
                image,
                f"face {i}:{confidence:.2f}",
                (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )
        success,encoded_img=cv2.imencode('.png',image)
        

    elif conversionId=='e3':
        yolomodel=get_yolo_model()
        results=yolomodel(image)
            
        annotated=image.copy()
        object_counts={}  
        class_names=yolomodel.names 
        for result in results:
            for box in result.boxes:
                cls_id=int(box.cls[0])
                cls_name=class_names[cls_id]

                if cls_name in object_counts:
                    object_counts[cls_name]+=1
                else:
                    object_counts[cls_name]=1

                confidence=float(box.conf[0])
                x1,y1,x2,y2=map(int,box.xyxy[0])
                cv2.rectangle(
                    annotated,
                    (x1,y1),
                    (x2,y2),
                    (0,255,0),
                    2
                )
                cv2.putText(
                    annotated,
                    f"{cls_name} {confidence:.2f}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )   
        
        headers["X-Objects-Counts"]=json.dumps(object_counts)
        
        success,encoded_img=cv2.imencode('.png',annotated)

    elif conversionId=='e4':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edge=cv2.Canny(gray,100,200)
        success,encoded_img=cv2.imencode('.png',edge)

    if not success:
        return ("500 server Error")
    
    return Response(content=encoded_img.tobytes(),media_type="image/png",headers=headers)
