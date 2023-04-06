import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './SideBar.css'

function SideBar(){
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'Side-bar-item-active' : '';
    }
    return (
        <nav className="Side-bar">
            <ul>
                {/* <Link className='Side-bar-item' to='/' activeclassname='Side-bar-item-active'>HOME</Link>
                <Link className='Side-bar-item' to='/img-detection' activeclassname='Side-bar-item-active'>IMAGE DETECTION</Link>
                <Link className='Side-bar-item' to='/video-detection' activeclassname='Side-bar-item-active'>VIDEO DETECTION</Link>
                <Link className='Side-bar-item' to='/contact' activeclassname='Side-bar-item-active'>CONTACT</Link> */}
                <Link className={`Side-bar-item ${isActive('/')}`}  to='/' activeclassname='Side-bar-item-active'>HOME</Link>
                <Link className={`Side-bar-item ${isActive('/img-detection')}`}  to='/img-detection' activeclassname='Side-bar-item-active'>IMAGE DETECTION</Link>
                <Link className={`Side-bar-item ${isActive('/video-detection')}`}  to='/video-detection' activeclassname='Side-bar-item-active'>VIDEO DETECTION</Link>
                {/* <Link className={`Side-bar-item ${isActive('/contact')}`}  to='/contact' activeclassname='Side-bar-item-active'>CONTACT</Link> */}
            </ul>
        </nav>
    );
};

export default SideBar