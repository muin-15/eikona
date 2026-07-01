
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
  paraValue:'bgr1'

});

mountUploadBox('bgr2',{
  id:'bgr2',
  title:'GRAY TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr2'
});

mountUploadBox('bgr3',{
  id:'bgr3',
  title:'BGR TO HSV',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr3'
});

mountUploadBox('bgr4',{
  id:'bgr4',
  title:'HSV TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr4'
});

mountUploadBox('bgr5',{
  id:'bgr5',
  title:'BGR TO RGB',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr5'
});

mountUploadBox('bgr6',{
  id:'bgr6',
  title:'RGB TO BGR',
  endpoint:'/color_conversion',
  paraName:'conversionId',
  paraValue:'bgr6'
});

mountUploadBox('filter1',{
  id:'filter1',
  title:'Mean Filtering',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter1'
});

mountUploadBox('filter2',{
  id:'filter2',
  title:'Median filtering',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter2'
});

mountUploadBox('filter3',{
  id:'filter3',
  title:'Gaussian Smoothing',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter3'
});

mountUploadBox('filter4',{
  id:'filter4',
  title:'laplacian Sharpening',
  endpoint:'/filtering',
  paraName:'conversionId',
  paraValue:'filter4'
});

mountUploadBox('t6',{
  id:'t6',
  title:'Uniform Image Scaling (UpScaling)',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t6'
});

mountUploadBox('t7',{
  id:'t7',
  title:'Uniform Image scaling (Downscaling)',
  endpoint:'/transformations',
  paraName:'conversionId',
  paraValue:'t7'
});

mountUploadBox('d2',{
  id:'d2',
  title:'Edge Detection',
  endpoint:'/detection',
  paraName:'conversionId',
  paraValue:'d2'
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
  }
});
