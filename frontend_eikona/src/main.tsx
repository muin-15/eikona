
import React, { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; 
import UploadBox from './App.tsx';

const mountUploadBox=(mountId:string,props:React.ComponentProps<typeof UploadBox> )=>{
const rootElement = document.getElementById(mountId);

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <UploadBox {...props}
      />
    </React.StrictMode>
  );
}else{
  console.error(`can't procide through element hook ID ${mountId}`);
}
};

mountUploadBox('bgr1',{
  id:'bgr1',
  title:'BGR To GRAY',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr1',
  requiredInput:1
});

mountUploadBox('bgr2',{
  id:'bgr2',
  title:'GRAY TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr2',
  requiredInput:1
});

mountUploadBox('bgr3',{
  id:'bgr3',
  title:'BGR TO HSV',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr3',
  requiredInput:1
});

mountUploadBox('bgr4',{
  id:'bgr4',
  title:'HSV TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr4',
  requiredInput:1
});

mountUploadBox('bgr5',{
  id:'bgr5',
  title:'BGR TO RGB',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr5',
  requiredInput:1
});

mountUploadBox('bgr6',{
  id:'bgr6',
  title:'RGB TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr6',
  requiredInput:1
});

mountUploadBox('filter1',{
  id:'filter1',
  title:'Mean Filtering',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter1',
  requiredInput:1
});

mountUploadBox('filter2',{
  id:'filter2',
  title:'Median filtering',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter2',
  requiredInput:1
});

mountUploadBox('filter3',{
  id:'filter3',
  title:'Gaussian Smoothing',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter3',
  requiredInput:1
});

mountUploadBox('filter4',{
  id:'filter4',
  title:'laplacian Sharpening',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter4',
  requiredInput:1
});

mountUploadBox('filter5',{
  id:'filter5',
  title:'Bilateral Filtering',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter5',
  requiredInput:1
});

mountUploadBox('t6',{
  id:'t6',
  title:'Uniform Image Scaling (UpScaling)',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t6',
  requiredInput:1
});

mountUploadBox('t7',{
  id:'t7',
  title:'Uniform Image scaling (Downscaling)',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t7',
  requiredInput:1
});

mountUploadBox('d2',{
  id:'d2',
  title:'Edge Detection',
  endpoint:'/detection',
  paraName:'conversionId',
  paraValue:'d2',
  requiredInput:1
});

mountUploadBox('compress-mount',{
  id:'compression',
  title:'Click to select Image',
  endpoint:'/compress',
  paraName:'conversionId',
  paraValue:'compress',
  range:{
    paraName:'intensity',
    elementId:'rangeInput'
  },
  requiredInput:1
});

mountUploadBox('histogram',{
  id:'histogram',
  title:'Image Histogram',
  endpoint:'/analytics',
  paraName:'conversionId',
  paraValue:'histogram',
  requiredInput:1
});

mountUploadBox('dft',{
  id:'dft',
  title:'Discrete Fourier Transform',
  endpoint:'/analytics',
  paraName:'conversionId',
  paraValue:'dft',
  requiredInput:1
});

mountUploadBox('dct',{
  id:'dct',
  title:'Discrete Cosine Transform',
  endpoint:'/analytics',
  paraName:'conversionId',
  paraValue:'dct',
  requiredInput:1
});

mountUploadBox('fft',{
  id:'fft',
  title:'Fast Fourier Transform',
  endpoint:'/analytics',
  paraName:'conversionId',
  paraValue:'fft',
  requiredInput:1
});

mountUploadBox('add',{
  id:'add',
  title:' Image Addition: First Image + ',
  endpoint:'/operations',
  paraName:'conversionId',
  paraValue:'add',
  requiredInput:2
});

mountUploadBox('sub',{
  id:'sub',
  title:'Image Subtraction: First Image - ',
  endpoint:'/operations',
  paraName:'conversionId',
  paraValue:'sub',
  requiredInput:2
});

mountUploadBox('mul',{
  id:'mul',
  title:'Image Multiplication: First Image * ',
  endpoint:'/operations',
  paraName:'conversionId',
  paraValue:'mul',
  requiredInput:2
});

mountUploadBox('div',{
  id:'div',
  title:'Image Division: First Image / ',
  endpoint:'/operations',
  paraName:'conversionId',
  paraValue:'div',
  requiredInput:2
});

mountUploadBox('t1',{
  id:'t1',
  title:'Image Rotation',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t1',
  requiredInput:3
});

mountUploadBox('t2',{
  id:'t2',
  title:'Background Removal',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t2',
  requiredInput:1
});

mountUploadBox('topng',{
  id:'topng',
  title:'Convert to PNG',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'topng',
  requiredInput:1
});

mountUploadBox('tojpg',{
  id:'tojpg',
  title:'Convert to JPG',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'tojpg',
  requiredInput:1
});

mountUploadBox('tobmp',{
  id:'tobmp',
  title:'Convert to BMP',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'tojpg',
  requiredInput:1
});

mountUploadBox('totiff',{
  id:'totiff',
  title:'Convert to TIFF',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'totiff',
  requiredInput:1
});

mountUploadBox('towebp',{
  id:'towebp',
  title:'Convert to WEBP',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'towebp',
  requiredInput:1
});