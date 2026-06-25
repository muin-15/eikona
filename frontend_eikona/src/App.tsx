import React,{ type ChangeEvent } from 'react' 
import './App.css'

const UploadBox = ({ id, title }: { id: string; title: string }) => {
  
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
      <UploadBox id="upload1" title="Upload Box 1" />
      <UploadBox id="upload2" title="Upload Box 2" />
    </div>
  )
}