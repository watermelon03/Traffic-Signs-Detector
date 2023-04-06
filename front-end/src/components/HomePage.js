import React, { useEffect, useState } from "react";
import axios from 'axios';
import './HomePage.css';
import PopupLoad from "./PopupLoad";

function HomePage(){
    const [detailAcc, setDetailAcc] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        onGetBaseAcc();
    }, [])

    const onGetBaseAcc = async() => {
        console.log("Get-Base-Acc")
        try{
            const response = await axios.get("http://localhost:5000/testGetAccuracy");
            setDetailAcc(response.data);
        }catch(error){
            console.log(error);
        }
    }

    const onGetAccClick = async(event) => {
        event.preventDefault();
        setIsLoading(true);
        console.log("Get-Acc")

        try{
            let formData = new FormData();
            formData.append("text", "web-acc");

            const response = await axios.post("http://localhost:5000/testPostAccuracy", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // console.log(response.data.imageTotal);
            setDetailAcc(response.data);
        }catch(error){
            console.log(error);
        }
        setIsLoading(false)
    }

    let accurate = null;
    if(detailAcc){
        accurate = 
        <div>
            <div>
                {Object.entries(detailAcc).map(([key, value]) => (
                    <p key={key}>{`${key}: ${value}`}</p>
                ))}
            </div>
        </div>
    }

    let load = null;
    if(isLoading){
       load = <PopupLoad />
    }

    return(
        <div className="Home-contrainer">
            <div className='Home-header'>
                <h2>HOME PAGE</h2>
            </div>
            <div className="Home-content">
                <div className="Home-content-left">
                    <h3>Traffic Signs Detection System</h3>
                    <p>
                        ระบบตรวจจับประเภทของป้ายจราจร เป็นระบบที่สามารถตรวจจับว่า 
                        ป้ายจราจรที่แสดงอยู่ในรูปภาพหรือวิดีโอเป็นป้ายจราจรประเภทใด 
                        และยังสามารถบอกลักษณะรูปร่างและสีของป้ายจราจรนั้นได้อีกด้วย
                    </p>
                    <img src="image/pngegg.png" alt="ImgHeader" />
                </div>
                <div className="Home-content-right">
                    <h3>Average Accuracy</h3>
                    {accurate}
                </div>
            </div>
            <div className="Home-button">
                <button className="Home-button-get" onClick={onGetAccClick}>Last Accuracy</button>
            </div>
            <div>
                {load}
            </div>
        </div>
    )
}

export default HomePage