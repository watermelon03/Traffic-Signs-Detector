import React, { useState } from "react";
import './VideoOutput.css'
import PopupWarn from "./PopupWarn";


function VideoOutput(probs) {
    const [shapeVideo, setShapeVideo] = useState(false);
    const [isWarning, setIsWarning] = useState(false);

    const onVideoDownloadClick = () => {
        const a = document.createElement('a');
        if(shapeVideo){
            if(probs.vidShapeOutUrl !== ' '){
                a.href = probs.vidShapeOutUrl;
                a.download = "shape_detect_" + probs.vidShapeOutFile.name;
            }else{
                console.log("Please select video");
                return;
            }
        }else{
            if(probs.vidTypeOutUrl !== ' '){
                a.href = probs.vidTypeOutUrl;
                a.download = "type_detect_" + probs.vidTypeOutFile.name;
            }else{
                setIsWarning(true)
                return;
            }
        }
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    function onNextClick(){
        if(shapeVideo){
            setShapeVideo(false)
        }else{
            setShapeVideo(true)
        }
    }

    let vidOutput = null;
    let tag = null;
    let toButton = null;
    if(shapeVideo){
        if(probs.vidShapeOutUrl !== ' '){
            tag = <p>Shape Detection Video</p>
            vidOutput = <video controls src={probs.vidShapeOutUrl} alt="VideoShapeOut" />
            toButton = <button className="Video-content-output-to" onClick={onNextClick}>Back</button>
        }else{
            tag = <p>Video Detection</p>
        }
    }else{
        if(probs.vidTypeOutUrl !== ' '){
            tag = <p>Type Detection Video</p>
            vidOutput = <video controls src={probs.vidTypeOutUrl} alt="VideoTypeOut" />
            toButton = <button className="Video-content-output-to" onClick={onNextClick}>Next</button>
        }else{
            tag = <p>Video Detection</p>
        }
    }

    let warn = null;
    if(isWarning){
       warn = <PopupWarn onWarnClose={() => setIsWarning(false)} />
    }
    
  return (
    <div className="Video-content-output">
        <div>
            {tag}
            <p className="Video-content-output-video">
                {vidOutput}
            </p>
            <p>
                {/* <button className="Video-content-output-button" onClick={() => setPopupOpen(true)}>Detail</button> */}
                <button className="Video-content-output-button" onClick={onVideoDownloadClick}>Download</button>
                {/* {toButton} */}
            </p>
        </div>
        <div>
            {warn}
        </div>
    </div>
  )
}

export default VideoOutput