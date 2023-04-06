import React, { useEffect } from "react";
import './PopupDetail.css';

function PopupDetail(probs){
    // useEffect(() => {
    //     console.log('Popup Start');
    //     return() => {
    //         console.log('Popup End');
    //     }
    // }, []);

    const onImgDownloadClick = () => {
        const a = document.createElement('a');
        if(probs.imgOutUrl !== ' '){
            a.href = probs.imgOutUrl;
            a.download = "detected_" + probs.imgOutFile.name;
        }else{
            console.log("Please select image");
            return;
        }
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    let imgOutput = null;
    if(probs.imgOutUrl !== ' '){
        imgOutput = <img src={probs.imgOutUrl} alt="ImgOut" />
    }

    let detail = null;
    if(probs.detailOut.length > 0){
        detail = 

        // <ul>
        //     {Object.entries(probs.detailOut[0]).map(([key, value]) => (
        //         <li key={key}>{`${key}: ${value}`}</li>
        //     ))}
        // </ul>

        // <ul>
        //     {probs.detailOut.map((item, index) => (
        //         <li key={index}>
        //             {Object.entries(item).map(([key, value]) => (
        //                 <li key={key}>{`${key}: ${value}`}</li>
        //             ))}
        //             {/* <h3>{item.number}</h3> */}
        //             {/* <p>{`${item.type}: ${item.shape}`}</p> */}
        //         </li>
        //     ))}
        // </ul>
        <div>
            {probs.detailOut.map((item, index) => (
                <div className="Output-detail" key={index}>
                    {Object.entries(item).map(([key, value]) => (
                        <p key={key}>{`${key}: ${value}`}</p>
                    ))}
                </div>
            ))}
        </div>
    }

    return(
       <div className="Popup-detail">
            <div className="Popup-detail-block">
                <div className="Popup-detail-block-header">
                    <h2>DETAIL</h2>
                </div>
                <div className="Popup-detail-block-content">
                    <div className="Popup-detail-block-content-img">
                        {imgOutput}
                        <p>
                            <button className="Popup-detail-block-content-button" onClick={onImgDownloadClick}>Download</button>
                        </p>
                    </div>
                    <div className="Popup-detail-block-content-info">
                        {detail}
                    </div>
                </div>
                <p>
                    <button className="Popup-detail-button" onClick={probs.onPopupClose}>Close</button>
                </p>
            </div>
            
       </div>
    )
}

export default PopupDetail