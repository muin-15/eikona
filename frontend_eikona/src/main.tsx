
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

mountUploadBox('e4',{
  id:'e4',
  title:'Edge Detection',
  endpoint:'/exclusive',
  paraName:'conversionId',
  paraValue:'e4',
  requiredInput:1
});

mountUploadBox('compress-mount',{
  id:'compression',
  title:'Click to select img',
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

mountUploadBox('tool1',{
  id:'tool1',
  title:'Background Removal',
  endpoint:'/tools',
  paraName:'conversionId',
  paraValue:'tool1',
  requiredInput:1
});

mountUploadBox('toconvert',{
  id:'topng',
  title:'Convert to Another File Format',
  endpoint:'/image_conversion',
  paraName:'conversionId',
  paraValue:'toconvert',
  requiredInput:1
});


mountUploadBox('t3',{
  id:'t3',
  title:'Negative Transformation',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t3',
  requiredInput:1
});

mountUploadBox('t4',{
  id:'t4',
  title:'Power-Law Transformation',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t4',
  requiredInput:4
});

mountUploadBox('t5',{
  id:'t5',
  title:'Log Transformation',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t5',
  requiredInput:1
});

mountUploadBox('res1',{
  id:'res1',
  title:'Inverse Filtering',
  endpoint:'/restoration',
  paraName:'conversionId',
  paraValue:'res1',
  requiredInput:6
});

mountUploadBox('res2',{
  id:'res2',
  title:'Wiener Filtering',
  endpoint:'/restoration',
  paraName:'conversionId',
  paraValue:'res2',
  requiredInput:6
});

mountUploadBox('tool2',{
  id:'tool2',
  title:'Stilyzation',
  endpoint:'/tools',
  paraName:'conversionId',
  paraValue:'tool2',
  requiredInput:5
});

mountUploadBox('tool3',{
  id:'tool3',
  title:'IMAGE INPAINT',
  endpoint:'/tools',
  paraName:'conversionId',
  paraValue:'tool3',
  requiredInput:1
});

mountUploadBox('tool4',{
  id:'tool4',
  title:'Pencil Sketch',
  endpoint:'/tools',
  paraName:'conversionId',
  paraValue:'tool4',
  requiredInput:5
});

mountUploadBox('tool5',{
  id:'tool5',
  title:'HDR EFFECT',
  endpoint:'/tools',
  paraName:'conversionId',
  paraValue:'tool5',
  requiredInput:5
});

mountUploadBox('d1',{
  id:'d1',
  title:'Thresholding(Binary)',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'d1',
  requiredInput:1
});

mountUploadBox('bgr7',{
  id:'bgr7',
  title:'BGR to LAB',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr7',
  requiredInput:1
});

mountUploadBox('bgr8',{
  id:'bgr8',
  title:'LAB to BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr8',
  requiredInput:1
});

mountUploadBox('e1',{
  id:'e1',
  title:'Quality Enhancement',
  endpoint:'/exclusive',
  paraName:'conversionId',
  paraValue:'e1',
  requiredInput:1
});

mountUploadBox('e2',{
  id:'e2',
  title:'Face Detection',
  endpoint:'/exclusive',
  paraName:'conversionId',
  paraValue:'e2',
  requiredInput:1
});

mountUploadBox('e3',{
  id:'e3',
  title:'Object Detection',
  endpoint:'/exclusive',
  paraName:'conversionId',
  paraValue:'e3',
  requiredInput:1
});