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
        setError(true);
        return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append(paraName, paraValue);

    if (range) {
        const rangeEl = document.getElementById(range.elementId) as HTMLInputElement;
      if (rangeEl) {
        formData.append(range.paraName, rangeEl.value);
      }
    }

    try {
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            setmessage(`Success: ${data?.message}`);
            setError(false);
        } else {
            setmessage(`Error: ${data?.detail || data?.message}`);
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

    {file && <p className="mt-2 text-green-400 text-sm">Selected: {file.name}</p>}

    <button onClick={handleSubmit} className='flex flex-col text-center items-center justify-center border-2 to-black bg-[#302b2b] hover:bg-[#3e3938] hover:text-white cursor-pointer rounded-md w-44 h-12 mt-10 '>
      Submit
    </button>

    {message && (
      <p className={`mt-4 text-sm ${isError ? 'text-red-500' : 'text-green-500'}`}>
        {message}
      </p>
    )}
    </>
  );
}

export default UploadBox;