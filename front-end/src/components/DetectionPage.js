import React, { useRef, useState } from "react";
import axios from 'axios';
import DetectionInput from "./DetectionInput";
import DetectionOutput from "./DetectionOutput";
import './DetectionPage.css';
import PopupLoad from "./PopupLoad";
import PopupWarn from "./PopupWarn";

function DetectionPage() {
    const fileRef =useRef(null);
    const [imgInUrl, setImgInUrl] =  useState(' ');
    const [imgInFile, setImgInFile] =  useState(null);
    const [imgOutUrl, setImgOutUrl] =  useState(' ');
    const [imgOutFile, setImgOutFile] =  useState(null);
    const [detailOut, setDetailOut] =  useState(null);

    const [isLoading, setIsLoading] = useState(false);
    const [isWarning, setIsWarning] = useState(false);

    function onUploadfileClick(){
        const myFileImgIn = fileRef.current.files[0];

        if(!myFileImgIn){
            // console.log("Please select image");
            setIsWarning(true)
            return;
        }
        setImgInFile(myFileImgIn)
        setImgInUrl(URL.createObjectURL(myFileImgIn));
        setImgOutUrl(' ')
        setImgOutFile(null);
    }

    let controller = new AbortController();
    const onSendfileClick = async(event) => {
        event.preventDefault();

        if(!imgInFile){
            setIsWarning(true)
            return;
        }

        setIsLoading(true);
        const myFileImgOut = imgInFile;
        try{
            const signal = controller.signal;

            let formData = new FormData();            
            formData.append("image", myFileImgOut);
            formData.append("text", "web-detect");

            const response = await axios.post("http://localhost:5000/testPostDetector", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                signal,
            });
            // console.log(response.data.text[1].main_text);

            const detail = response.data.objectInfo
            
            const imageUrl = `data:image/jpeg;base64,${response.data.imagePath}`;
            const fileName = imgInFile.name;

            const outputFile = new File([imageUrl], fileName, { type: "image/jpeg" });
            // console.log("imageOutput: ",outputFile);

            setImgOutFile(outputFile);
            setImgOutUrl(imageUrl);
            setDetailOut(detail);

        }catch(error){
            console.log(error);
            if(error.name === "AboutError"){
                console.log("API have cancelled")
            }else if(axios.isCancel(error)) {
                console.log("Request was cancelled by axios");
            }else{
                console.log("Request failed:", error);
            }
        }finally{ 
            setIsLoading(false);
        }
    }
    
    const onCancelClick = () => {
        controller.abort();
        console.log("Cancelled by user");
    }

    function onClearClick(){
        setImgInUrl(' ');
        setImgOutUrl(' ');
        setImgInFile(null);
        setImgOutFile(null);
    }

    let load = null;
    if(isLoading){
       load = <PopupLoad onCancelClick={onCancelClick} />
    }
    let warn = null;
    if(isWarning){
       warn = <PopupWarn onWarnClose={() => setIsWarning(false)}/>
    }

  return (
    <div className="Detection-contrainer">
        <div className='Detection-header'>
            <h2>IMAGE DETECTION PAGE</h2>
        </div>
        <div className="Detection-content">
            <DetectionInput imgInUrl={imgInUrl} onUploadfileClick={onUploadfileClick} ref={fileRef} />
            <DetectionOutput imgOutFile={imgOutFile} imgOutUrl={imgOutUrl} detailOut={detailOut} />
        </div>
        <div className="Detection-button">
            <button className="Detection-button-submit" onClick={onSendfileClick}>Submit</button>
            <button className="Detection-button-clear" onClick={onClearClick}>Clear</button>
        </div>
        <div>
            {load}
            {warn}
        </div>
    </div>
  )
}

export default DetectionPage
