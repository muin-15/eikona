
import React, { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; 
import UploadBox from './App.tsx';

const mountUploadBox=(mountId:string,props:React.ComponentProps<typeof UploadBox> )=>{

  const rootelement=document.getElementById(mountId);
  if(rootelement){
    ReactDOM.createRoot(rootelement).render(
      <StrictMode>
        <UploadBox {...props}/>
      </StrictMode>,
    );
  }
  else{
    console.error(`Can't procide through ${mountId}`);
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