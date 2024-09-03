import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Components/login'
import AdminDashboard from './Components/AdminDashboard'
import UserRegistration from './Components/userRegisteration';

function App() {

  return (
    <Router>
    <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<AdminDashboard />} />
        <Route path="/register" element={<UserRegistration />} />
    </Routes>
</Router>
  )
}

export default App
