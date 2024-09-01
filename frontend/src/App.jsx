import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Login from './Components/login'
import AdminDashboard from './Components/AdminDashboard'

function App() {

  return (
    <div>
      <Login/>
      <AdminDashboard/>

    </div>
  )
}

export default App
