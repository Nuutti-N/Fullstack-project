import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import Analyze from "./pages/Analyze"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/analyze" element={<Analyze />} />
        {/* <Route path="/history" element={<History />} /> */}


      </Routes>
    </BrowserRouter>)
}


export default App
