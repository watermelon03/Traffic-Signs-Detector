import React from "react";
import './PopupLoad.css';

function PopupLoad(probs){

    return(
       <div className="Popup-load">
            <div className="Popup-load-block">
                <img src="image/loading-progress-bar-vector-tim-hester-transparent.png" alt="ImgLoad" />
                {/* <button className="Video-button-clear" onClick={probs.onCancelClick}>Cancel</button> */}
            </div>
            
       </div>
    )
}

export default PopupLoad