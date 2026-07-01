import React,{ useState, type ChangeEvent } from 'react' 
import './App.css'

interface prop_uploadbox{
  id:string;
  title:string
  endpoint:string
  paraName:string
  paraValue:string
  range?:{
    paraName:string
    elementId:string
  }
}
const UploadBox:React.FC<prop_uploadbox> = ({ id, title ,endpoint,paraName,paraValue,range}) => {
  const [message,setmessage]= useState<string>('');
  const [isError,setError]=useState<boolean>(false);
  const [file,setFile]=useState<File | null>(null);

  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>) => {
    console.log("Event handling is processing");
    const selectedFile=event.target.files?.[0];
    if(selectedFile){
      setFile(selectedFile);
    }
  };

  const handleSubmit = async () => {

    if (!file) {
        setmessage("Please select an image.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append(paraName, paraValue);

    if (range) {
        const rangeEl = document.getElementById(range.elementId) as HTMLInputElement;

        formData.append(range.paraName, rangeEl.value);
    }

    try {
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            setmessage(`Success: ${data.message}`);
            setError(false);
        } else {
            setmessage(`Error: ${data.detail || data.message}`);
            setError(true);
        }

    } catch (err) {
        setmessage(`Network Error: ${err instanceof Error ? err.message : String(err)}`);
        setError(true);
    }
};
  
  return (
    <>
    <label htmlFor={id} className="upload-box ">
      {title}
      <input type="file" id={id} onChange={handlefilechange} className="hidden" />
    </label>
    <button onClick={handleSubmit} className='flex flex-col text-center items-center justify-center border-2 to-black bg-[#3D3838] hover:bg-[#2d2928] hover:text-white cursor-pointer rounded-md w-44 h-12 mt-10'>
      Submit
    </button>
    </>
  );
}

export default UploadBox;