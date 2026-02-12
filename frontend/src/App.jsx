import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import ChatWidget from './ChatWidget'

function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Mon Assistant Assurance</h1>
      <hr />
      <ChatWidget />
    </div>
  )
}

export default App