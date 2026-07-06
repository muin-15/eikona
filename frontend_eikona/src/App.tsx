import React,{ useState, type ChangeEvent } from 'react' 
import './App.css'

interface prop_uploadbox{
  id:string;
  title:string;
  endpoint:string;
  paraName:string;
  paraValue:string;
  requiredInput?:number;
  range?:{
    paraName:string;
    elementId:string;
  };
}
const UploadBox:React.FC<prop_uploadbox> = ({ 
  id, title, endpoint, paraName, paraValue, range,requiredInput=1,
}) => {
  const [message,setmessage]= useState<string>('');
  const [isError,setError]=useState<boolean>(false);
  const [file,setFile]=useState<File | null>(null);
  const [file2,setFile2]=useState<File | null>(null);
  const [angle,setAngle]=useState<number | null>(null);

  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>,type:'file' | 'file2') => {
    console.log("Event handling is processing");
    const selectedFile=event.target.files?.[0];
    if(selectedFile){
      if(type==='file'){
        setFile(selectedFile);
      } else {
        setFile2(selectedFile);
      }
    }
  };

  const handleSubmit = async () => {

    if (!file) {
        setmessage("Please select an image.");
        setError(true);
        return;
    }
    if (requiredInput === 2 && !file2) {
        setmessage("Please select the second image.");
        setError(true);
        return;
    }
    if (requiredInput === 3 && angle===null){
      setmessage("Please enter angle to rotate");
      setError(true);
      return;
    }
    const formData = new FormData();

    formData.append("file", file);
    if(requiredInput===2 && file2){
      formData.append("file2", file2);
    }
    if(requiredInput===3 && angle !==null){
      formData.append("angle",angle.toString());
    }
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
      <input type="file" id={id}  className="hidden" onChange={(e) => handlefilechange(e, "file")} />
    </label>
   {requiredInput === 2 && (
    <label htmlFor={`${id}-2`} className="upload-box border-4 border-dashed border-white rounded-md p-4 mt-4">
        Second Image
        <input
            id={`${id}-2`}
            type="file"
            className="hidden"
            onChange={(e) => handlefilechange(e, "file2")}
        />
    </label>
    )}
    {requiredInput===3 && (
      <div className="mt-4">
      <label htmlFor={`${id}-3`} className="block mb-2">
        Enter Angle
      </label>

      <input
        id={`${id}-3`}
        type="number"
        className="border-2 rounded-md p-2 w-full"
        placeholder="e.g. 45"
        onChange={(e) => setAngle(Number(e.target.value))}
      />
</div>
    )}
    {file && <p className="mt-2 text-amber-300 text-sm">Selected: {file.name}</p>}

    <button onClick={handleSubmit} className='flex flex-col text-center items-center justify-center border-2 to-black bg-[#302b2b] hover:bg-[#3e3938]  hover:text-white cursor-pointer rounded-md w-54 h-12 mt-10 '>
      Submit
    </button>

    {message && (
      <p className={`mt-4 text-sm ${isError ? 'text-red-500' : 'text-amber-50'}`}>
        {message}
      </p>
    )}
    </>
  );
}

export default UploadBox;