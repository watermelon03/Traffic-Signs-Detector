import React, { useState } from "react";
import PopupDetail from './PopupDetail';
import './DetectionOutput.css'
import PopupWarn from "./PopupWarn";


function DetectionOutput(probs) {
    const [popupOpen, setPopupOpen] = useState(false);
    const [isWarning, setIsWarning] = useState(false);

    let popup = null;
    if(popupOpen){
        if(!probs.imgOutFile){
            setPopupOpen(false)
            setIsWarning(true)
            console.log("Please select image");
            return;
        }
       popup = <PopupDetail imgOutFile={probs.imgOutFile} imgOutUrl={probs.imgOutUrl} detailOut={probs.detailOut} onPopupClose={() => setPopupOpen(false)} />
    }

    let imgOutput = null;
    if(probs.imgOutUrl !== ' '){
        imgOutput = <img src={probs.imgOutUrl} alt="ImgOut" />
    }
    let warn = null;
    if(isWarning){
       warn = <PopupWarn onWarnClose={() => setIsWarning(false)} />
    }
  return (
    <div className="Detection-content-output">
        <div>
            <p className="Detection-content-output-img">
                {imgOutput}
            </p>
            <p>
                <button className="Detection-content-output-button" onClick={() => setPopupOpen(true)}>Detail</button>
            </p>
        </div>
        <div>
            {popup}
            {warn}
        </div>
    </div>
  )
}

export default DetectionOutput
// how to increase efficiency and accuracy