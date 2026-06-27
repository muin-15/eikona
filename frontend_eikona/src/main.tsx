
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css'; 
import UploadBox from './App.tsx';

const bgrconversionelement1=document.getElementById('bgr1');
const bgrconversionelement2=document.getElementById('bgr2');
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
} else {
  console.error("Failed to find the root element in the DOM. Ensure your index.html has a <div id='root'></div>");
}