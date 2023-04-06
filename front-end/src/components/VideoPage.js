import React, { useRef, useState } from "react";
import axios from 'axios';
import './VideoPage.css';
import VideoInput from "./VideoInput";
import VideoOutput from "./VideoOutput";
import PopupLoad from "./PopupLoad";
import PopupWarn from "./PopupWarn";

function VideoPage() {
    const vidRef =useRef(null);
    const [vidInUrl, setVidInUrl] =  useState(' ');
    const [vidInFile, setVidInFile] =  useState(null);
    const [vidTypeOutUrl, setVidTypeOutUrl] =  useState(' ');
    const [vidTypeOutFile, setVidTypeOutFile] =  useState(null);
    const [vidShapeOutUrl, setVidShapeOutUrl] =  useState(' ');
    const [vidShapeOutFile, setVidShapeOutFile] =  useState(null);

    const [isLoading, setIsLoading] = useState(false);
    const [isWarning, setIsWarning] = useState(false);

    function onUploadfileClick(){
        const myFileVidIn = vidRef.current.files[0];

        if(!myFileVidIn){
            setIsWarning(true)
            return;
        }
        
        setVidInFile(myFileVidIn)
        setVidInUrl(URL.createObjectURL(myFileVidIn));
        console.log("videoInput: ", myFileVidIn);
        
        setVidTypeOutUrl(' ')
        setVidTypeOutFile(null);
        setVidShapeOutUrl(' ')
        setVidShapeOutFile(null);
    }

    const onSendfileClick = async(event) => {
        event.preventDefault();

        if(!vidInFile){
            setIsWarning(true)
            return;
        }
        
        setIsLoading(true);
        const myFileVideoOut = vidInFile;
        try{
            let formData = new FormData();            
            formData.append("video", myFileVideoOut);
            formData.append("text", "web-video");

            const response = await axios.post("http://localhost:5000/testPostVideo", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            console.log(response.data.state);
            
            const typeUrl = `data:video/mp4;base64,${response.data.typePath}`;
            const typeFilename = "type_detect_" + vidInFile.name;

            const typeFile = new File([typeUrl], typeFilename, { type: "video/mp4" });
            console.log("typeOutput: ",typeFile);

            setVidTypeOutUrl(typeUrl);
            setVidTypeOutFile(typeFile);

        }catch(error){
            console.log(error);
        }
        setIsLoading(false);
    }

    function onClearClick(){
        setVidInUrl(' ');
        setVidInFile(null);
        setVidTypeOutUrl(' ')
        setVidTypeOutFile(null);
        setVidShapeOutUrl(' ')
        setVidShapeOutFile(null);
    }

    let load = null;
    if(isLoading){
       load = <PopupLoad />
    }
    let warn = null;
    if(isWarning){
       warn = <PopupWarn onWarnClose={() => setIsWarning(false)} />
    }

  return (
    <div className="Video-contrainer">
        <div className='Video-header'>
            <h2>VIDEO DETECTION PAGE</h2>
        </div>
        <div className="Video-content">
            <VideoInput vidInUrl={vidInUrl} onUploadfileClick={onUploadfileClick} ref={vidRef} />
            <VideoOutput vidTypeOutFile={vidTypeOutFile} vidTypeOutUrl={vidTypeOutUrl} 
            vidShapeOutFile={vidShapeOutFile} vidShapeOutUrl={vidShapeOutUrl}/>
        </div>
        <div className="Video-button">
            <button className="Video-button-submit" onClick={onSendfileClick}>Submit</button>
            <button className="Video-button-clear" onClick={onClearClick}>Clear</button>
        </div>
        <div>
            {load}
            {warn}
        </div>
    </div>
  )
}

export default VideoPage
