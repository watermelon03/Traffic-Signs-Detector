import React from 'react'
import './VideoInput.css'

const VideoInput = React.forwardRef((probs, vidRef) =>{
    let vidInput = null;
    if(probs.videoInUrl !== ' '){
        vidInput = <video controls src={probs.vidInUrl} alt="VideoIn" />
    }

  return (
    <div className="Video-content-input">
        <p className="Video-content-input-video">
            {vidInput}
        </p>
        <p>
            <input type="file" accept="video/mp4" ref={vidRef} />
        </p>
        <p>
            <button className="Video-content-input-button" onClick={probs.onUploadfileClick}>Confirm</button>
        </p>
    </div>
  )
});

export default VideoInput