import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import Analyze from "./pages/Analyze"
import History from "./pages/History"
import PrivateRoute from "./components/PrivateRoutes"
import NavBar from "./components/Navbar/NavBar"


function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route element={<PrivateRoute />}>
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/history" element={<History />} />
        </Route>

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>)
}


export default App
