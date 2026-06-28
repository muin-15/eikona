import React,{ type ChangeEvent } from 'react' 
import './App.css'

const UploadBox = ({ id, title ,conversionId}: { id: string; title: string; conversionId:string }) => {
  
  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>) => {
    console.log("Event handling is processing");
    const file=event.target.files?.[0]
    if(!file) return

    const formData=new FormData()
    formData.append('file',file);
    formData.append("conversionId",conversionId);

    try{
      const response=await fetch('http://localhost:8000/color_conversion', {
        method: 'POST',
        body: formData
      })
      //const response=await fetch('http://localhost:8000/color_conversion')
      const data=await response.json()
      console.log('File uploaded successfully:', data)
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  };
  return (
    <label htmlFor={id} className="upload-box">
      {title}
      <input type="file" id={id} onChange={handlefilechange} className="hidden" />
    </label>
  )
}

export default UploadBox;