import React,{ useState, type ChangeEvent } from 'react' 
import './App.css'

interface prop_uploadbox{
  id:string;
  title:string
  endpoint:string
  paraName:string
  paraValue:string
}
const UploadBox:React.FC<prop_uploadbox> = ({ id, title ,endpoint,paraName,paraValue}) => {
  const [message,setmessage]= useState<string>('');
  const [isError,setError]=useState<boolean>(false);

  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>) => {
    console.log("Event handling is processing");
    setmessage('');
    setError(false);
    const file=event.target.files?.[0]
    if(!file) {
      setmessage("No File return")
      return;
    }
    const formData=new FormData()
    formData.append('file',file);
    formData.append(paraName,paraValue);

    try{
      const response=await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        body: formData
      })
      const data=await response.json()
      if (response.ok){
        setmessage(`Success:${data.message}`);
        setError(false);
      }
      else{
        setmessage(`Error:${data.detail || data.message}`);
        setError(true)
      }
      console.log('File uploaded successfully:', data)
    } catch (error) {
      setmessage(`network Error ${error instanceof Error ? error.message:String(error)}`)
      console.error('Error uploading file:', error)
    }
  };
  return (
    <label htmlFor={id} className="upload-box ">
      {title}
      <input type="file" id={id} onChange={handlefilechange} className="hidden" />
    </label>
  )
}

export default UploadBox;