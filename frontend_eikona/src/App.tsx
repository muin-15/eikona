import React,{ type ChangeEvent } from 'react' 
import { useState } from 'react'
import './App.css'

const UploadBox = ({ id, title ,conversionId}: { id: string; title: string; conversionId:string }) => {
  
  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>) => {
    const file=event.target.files?.[0]
    if(!file) return

    const formData=new FormData()
    formData.append('file',file)

    try{
      const response=await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })
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

export default function App() {
  return (
    <div>
      <UploadBox id="bgr" title="Upload Box 1" conversionId="bgr1"/>
    </div>
  )
}