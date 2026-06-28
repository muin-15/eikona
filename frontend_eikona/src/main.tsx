
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css'; 
import UploadBox from './App.tsx';

const bgrconversionelement1=document.getElementById('bgr1');
const bgrconversionelement2=document.getElementById('bgr2');
const bgrconversionelement3=document.getElementById('bgr3');
const bgrconversionelement4=document.getElementById('bgr4');
const bgrconversionelement5=document.getElementById('bgr5');
const bgrconversionelement6=document.getElementById('bgr6');
if (bgrconversionelement1) {
  ReactDOM.createRoot(bgrconversionelement1).render(
    <React.StrictMode>
      <UploadBox 
      id="bgr_grayconvert"
      title="BGR to GRAY"
      conversionId="bgr1"
      />
    </React.StrictMode>,
  );
if (bgrconversionelement2){
  ReactDOM.createRoot(bgrconversionelement2).render(
    <React.StrictMode>
      <UploadBox
      id="gray_bgrconvert"
      title="GRAY TO BGR"
      conversionId="bgr2"
      />
    </React.StrictMode>
  );
}
if(bgrconversionelement3){
  ReactDOM.createRoot(bgrconversionelement3).render(
    <React.StrictMode>
      <UploadBox
      id="bgr3"
      title="BGR TO HSV"
      conversionId="bgr3"
      />
    </React.StrictMode>
  );
}
if(bgrconversionelement4){
  ReactDOM.createRoot(bgrconversionelement4).render(
    <React.StrictMode>
      <UploadBox
      id="bgr4"
      title="HSV TO BGR"
      conversionId="bgr4"
      />
    </React.StrictMode>
  );
}
if(bgrconversionelement5){
  ReactDOM.createRoot(bgrconversionelement5).render(
    <React.StrictMode>
      <UploadBox
      id="bgr5"
      title="BGR TO RGB"
      conversionId="bgr5"
      />
    </React.StrictMode>
  );
}
if(bgrconversionelement6){
  ReactDOM.createRoot(bgrconversionelement6).render(
    <React.StrictMode>
      <UploadBox
        id="bgr6"
        title="RGB TO BGR"
        conversionId="bgr6"
      />
    </React.StrictMode>
  )
}
} else {
  console.error("Failed to find the root element in the DOM. Ensure your index.html has a <div id='root'></div>");
}