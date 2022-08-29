import React, { useState, useEffect } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Nav from '../components/Nav';

export default function App() {
  const getUserFromLocalStorage = () => {
    const foundUser = localStorage.getItem('user')
    if (foundUser){
      return JSON.parse(foundUser)
    }
    return {}
  };

  const [user, setUser] = useState(getUserFromLocalStorage())
  const [cart, setCart] = useState([])

  const logMeIn = (user) => {
    setUser(user)
    localStorage.setItem('user', JSON.stringify(user))
  }

  const logMeOut = () => {
    setUser({})
    localStorage.removeItem('user')
  }

  return (
    <BrowserRouter>
      <div>
      <Nav />
      
        <Routes>

        </Routes>

      </div>
    </BrowserRouter>
  )
}
