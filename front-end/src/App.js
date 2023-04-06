import React from 'react';
import {Route, Routes } from 'react-router-dom';
import AppFooter from './components/AppFooter';
import AppHeader from './components/AppHeader';
import ContactPage from './components/ContactPage';
import DetectionPage from './components/DetectionPage';
import ErrorPage from './components/ErrorPage';
import HomePage from './components/HomePage';
import SideBar from './components/SideBar';
import './App.css';
import VideoPage from './components/VideoPage';

function App() {
  return (
    <div className="App">
      <AppHeader />
      <div className='Contrainer'>
        <SideBar />
        <div className='Content'>
          <Routes>
            <Route exact path='/' element={<HomePage />} />
            <Route path='/img-detection' element={<DetectionPage />} />
            <Route path='/video-detection' element={<VideoPage />} />
            <Route path='/contact' element={<ContactPage />} />
            <Route path='*' element={<ErrorPage />} />
          </Routes>
        </div>
      </div>
      <AppFooter />
    </div>
  );
}

export default App;
