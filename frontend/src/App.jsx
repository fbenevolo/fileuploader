import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './index.css'

import NavBar from './NavBar.jsx'
import UploadFile from './UploadFile.jsx'
import StorageUsage from './StorageUsage.jsx'
import ListFiles from './ListFiles.jsx'

function App() {

  return (
    <>
      <NavBar/>
      <main className="p-stack-lg min-h-[calc(100vh-64px)] py-stack-lg">
          <div className="max-w-[1200px] mx-auto">
            <StorageUsage/>
            <UploadFile/>
            <ListFiles/>
          </div>
      </main>
    </>
  )
}

export default App