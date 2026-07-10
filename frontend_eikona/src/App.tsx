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
  const [gValue,setGvalue]=useState<number | null>(null);
  const [sigmaS,setSsigma]=useState<number | null>(null);
  const [sigmaR,setRsigma]=useState<number | null>(null);

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
    if (requiredInput === 4 && gValue===null){
      setmessage("Please enter Gamma value to transform");
      setError(true);
      return;
    }
    if (requiredInput === 5 && (sigmaR===null || sigmaS===null)){
      setmessage("please enter Sigma_s value");
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
    if(requiredInput===4 && gValue !==null){
      formData.append("gamma",gValue.toString())
    }
    if(requiredInput===5 &&  sigmaR!==null && sigmaS!==null){
      formData.append("sigmaS",sigmaS.toString())
      if(sigmaR){
      formData.append("sigmaR",sigmaR.toString()) 
      }
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
        Enter Angle to Rotate Image
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
    {requiredInput===4 && (
      <div className='mt-4'>
        <label htmlFor={`${id}-4`} className="block mb-2">
          Enter Gamma Value
        </label>

        <input
          id={`${id}-4`}
          type="number"
          className="border-2 rounded-md p-2 w-full "
          placeholder='bet: 0.1-5.0'
          onChange={(e) => setGvalue(Number(e.target.value))}
        />
      </div>
    )}
    {requiredInput===5 &&(
      <div className='mt-12'>
        <label htmlFor={`${id}-5`} className="block mb-2">
          Enter Sigma Spatial Value
        </label>

        <input
          id={`${id}-5`}
          type='number'
          className="border-2 rounded-md p-2 w-full"
          placeholder='bet: 1-100+'
          onChange={(e) => setSsigma(Number(e.target.value))}
        />
        <label htmlFor={`${id}-6`} className='block mb-2'>
          Enter Sigma Range
        </label>

        <input
          id={`${id}-6`}
          type='number'
          className='border-2 rounded-md p-2 w-full'
          placeholder='bet: 0.1-1.0'
          onChange={(e) => setRsigma(Number(e.target.value))}
        />
      </div>
    )

    }
    {file && <p className="mt-2 w-64 text-center text-amber-300 text-sm break-words mx-auto">Selected: {file.name}</p>}

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