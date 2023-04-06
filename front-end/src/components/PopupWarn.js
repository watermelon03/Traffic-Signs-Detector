import React from "react";
import './PopupWarn.css';

function PopupWarn(probs){

    return(
       <div className="Popup-Warn">
            <div className="Popup-Warn-block">
                <img src="image/1824224.png" alt="ImgWarn" />
                <h3>Please select image or video</h3>
                <p>
                    <button className="Popup-Warn-button" onClick={probs.onWarnClose}>Close</button>
                </p>
            </div>
            
            
       </div>
    )
}

export default PopupWarn