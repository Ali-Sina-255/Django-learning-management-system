import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Components/login'
import AdminDashboard from './Components/AdminDashboard'

function App() {

  return (
    <Router>
    <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<AdminDashboard />} />
    </Routes>
</Router>
  )
}

export default App
