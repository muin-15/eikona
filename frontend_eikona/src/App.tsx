import React,{ useState, type ChangeEvent } from 'react' 
import './App.css'
import {LoaderCircle} from "lucide-react"; 
import {Download} from "lucide-react";

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
  const [loading,setLoading]=useState<boolean>(false);
  const [preview,setPreview]=useState("");
  const [showpreview,setShowpreview]=useState(false);
  const [resultimage,setResultimage]=useState("");
  const [Resultview,setResultview]=useState(false);
  const [hidePreviewThumb,setHidePreviewThumb]=useState(false);
  const [hideResultThumb,setHideResultThumb]=useState(false);
  const [outputFormat,setOutputFormat]=useState('jpg');
  const [length,setLength]=useState<number | null>(null);

  const handlefilechange = async(event: ChangeEvent<HTMLInputElement>,type:'file' | 'file2') => {
    console.log("Event handling is processing");
    const selectedFile=event.target.files?.[0];
    if(!selectedFile) return;
    
    setShowpreview(true);
    if(selectedFile){
      if(type==='file'){
        setFile(selectedFile);
        setPreview(URL.createObjectURL(selectedFile));
      } else {
        setFile2(selectedFile);
        setPreview(URL.createObjectURL(selectedFile));
      }
      setHidePreviewThumb(false);
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
    if (requiredInput === 6 && (angle===null || length === null)){
      setmessage("please Enter Full Info");
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
      
      formData.append("sigmaR",sigmaR.toString()) 
    }
    if(requiredInput===6 && angle!==null && length!==null){
      formData.append("angle",angle.toString())
      formData.append("length",length.toString())
    }
    formData.append("outputFormat", outputFormat);
    formData.append(paraName, paraValue);

    if (range) {
        const rangeEl = document.getElementById(range.elementId) as HTMLInputElement;
      if (rangeEl) {

        formData.append(range.paraName, rangeEl.value);
      }
    }

    try {
        setLoading(true);
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method: "POST",
            body: formData,
        });
        
        if (response.ok) {
            const blob =await response.blob();
            const outputImage=URL.createObjectURL(blob)
            setResultimage(outputImage);
            setPreview("");
            setHideResultThumb(false);
            setmessage(`Success: Image Processed`);
            setError(false);

        } else {
            const errorText=await response.text()
            setmessage(`Error ${errorText}`);
            setError(true);
        }

    } catch (err) {
        setmessage(`Network Error: ${err instanceof Error ? err.message : String(err)}`);
        setError(true);
    }
    finally{
      setLoading(false);
      setShowpreview(false);
      setResultview(true);
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
    {requiredInput===6 &&(
      <div className='mt-12'>
        <label htmlFor={`${id}-7`} className='block mb-2'>
          Enter Angle for Restoration
        </label>
        <input
        id={`${id}-7`}
        type='number'
        className='border-2 rounded-md p-2 w-full'
        placeholder='eg:30'
        onChange={(e) => setAngle(Number(e.target.value))}
        />
        <label htmlFor={`${id}-8`} className='block mb-2'>
          Enter length for Restoration
        </label>
        <input
        id={`${id}-8`}
        type='number'
        className='border-2 rounded-md p-2 w-full'
        placeholder='eg:25'
        onChange={(e)=> setLength(Number(e.target.value))}
        />
      </div>
    )}
    <select
    value={outputFormat}
    onChange={(e) => setOutputFormat(e.target.value)}
    className="border-2 rounded-md p-2 mt-4 bg-black text-emerald-400"
    >
    <option value="jpg">JPG</option>
    <option value="png">PNG</option>
    <option value="bmp">BMP</option>
    <option value="tiff">TIFF</option>
    <option value="webp">WEBP</option>
    </select>
    <button onClick={handleSubmit} className=' text-center items-center justify-center border-2 to-black bg-[#302b2b] hover:bg-[#3e3938]  hover:text-white cursor-pointer rounded-md w-54 h-12 mt-10 '>
      Submit
    </button>
    {file && <p className="mt-2 w-64 text-center text-amber-300 text-sm wrap-break-words mx-auto">Selected: {file.name}</p>}

    {message && (
      <p className={`mt-4 text-sm ${isError ? 'text-red-500' : 'text-amber-50'}`}>
        {message}
      </p>
    )}
    {loading && (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex flex-col items-center justify-center">

      <LoaderCircle
          size={70}
          className="animate-spin text-emerald-400"
      />

      <p className="mt-6 text-xl text-white">
          Processing Image...
      </p>

      <p className="text-gray-400">
          Please wait
      </p>

    </div>
    )}
    {showpreview &&(
      <div className="fixed inset-0 bg-black/95 z-[9999] flex justify-center items-center"
      onClick={()=> setShowpreview(false)}>
        

        
        <img
        src={preview}
        alt="Full Preview"
        className="max-w-[90vw] max-h-[90vh] object-contain "
        onClick={(e)=>e.stopPropagation()}
      />

      <button
          onClick={()=> setShowpreview(false)}
          className="absolute top-5 right-5 text-white text-4xl hover:text-red-500">
            ✕
        </button>
        
        <button
          className="absolute bottom-28 right-8 bg-emerald-500 px-8 py-3 rounded-xl text-black font-bold hover:bg-emerald-400 border-black border-2"
          onClick={() => {setShowpreview(false);
                        setHidePreviewThumb(true);}}
        >
        Use Image
        </button>
        <button
          className="absolute bottom-8 right-8 bg-red-600 px-13 py-3 rounded-xl border-black border-2"
          onClick={() => {
          setShowpreview(false);
          setHidePreviewThumb(true);
          setFile(null);
          setPreview("");
      }}
      >
      Cancel
      </button>
      </div>
    )}
 {preview && !hidePreviewThumb && (
  <div className='mt-5'>
    <img
      src={preview}
      alt="Preview"
      onClick={() => setShowpreview(true)}
      className='w-54 border-2 border-black shadow-lg rounded-xl'
    />
  </div>
)}
  {resultimage && !hideResultThumb && (
    <div className='mt-8 flex flex-col items-center justify-center border-2 border-emerald-500 rounded-xl bg-emerald-950/20 w-full'>
    
    
    
    <img
      src={resultimage}
      className='max-w-xs  md:max-w-md border-2 border-emerald-400 shadow-[0_0_15px_rgba(52,211,153,0.5)] rounded-xl object-contain'
      onClick={()=>setResultview(true)}
    />

    </div>
    )}
    {resultimage && !loading &&(
          <a href={resultimage} download={`Eikona-Result-${Date.now()}.${outputFormat}`} className="mt-6 flex items-center px-4 py-4 bg-emerald-900 text-indigo-300 font-bold uppercase tracking-wider rounded-full hover:bg-emerald-950 hover:text-indigo-100 transition-colors">
            <Download size={20}/>
            </a>

    )}
    {Resultview &&(
      <div className="fixed inset-0 bg-black/95 z-[9999] flex justify-center items-center"
      onClick={()=> { setResultview(false); setHideResultThumb(true); }}>
       <img
        src={resultimage}
        alt="Full Preview"
        className="max-w-[90vw] max-h-[90vh] object-contain "
        onClick={(e)=>e.stopPropagation()}
      />

      <button
      onClick={()=> { setResultview(false); setHideResultThumb(true); }}
      className="absolute top-5 right-5 text-white text-4xl hover:text-red-500">
        ✕
      </button>
        
      </div>
    )}
    </>
  );
}

export default UploadBox;