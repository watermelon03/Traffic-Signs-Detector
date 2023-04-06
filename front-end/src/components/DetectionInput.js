import React from 'react'
import './DetectionInput.css'

const DetectionInput = React.forwardRef((probs, ref) =>{
    let imgInput = null;
    if(probs.imgInUrl !== ' '){
        imgInput = <img src={probs.imgInUrl} alt="ImgIn" />
    }

  return (
    <div className="Detection-content-input">
        <p className="Detection-content-input-img">
            {imgInput}
        </p>
        <p>
            <input type="file" accept="image/*" ref={ref} />
        </p>
        <p>
            <button className="Detection-content-input-button" onClick={probs.onUploadfileClick}>Confirm</button>
        </p>
    </div>
  )
});

export default DetectionInput