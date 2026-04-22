import "./NavBar.css"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import api from "../../api/client"

function NavBar() {
    const [Loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const navigate = useNavigate()
    useEffect(() => {
        function handleLogout() {
            setLoading(true)
            try {
                setError("")
                localStorage.removeItem('token')
                const response = api.get("/your")
                response.data
            }
            catch (err) {

            }
            finally {
                setLoading(false)
            }
            navigate("/login")
        }
    }, [])


    return (<> <nav> <button onClick={handleLogout}>Log out</button></nav>
        <div className="navbar">
            <h1>Trust the machine</h1>
            <ul className="nav-menu">
                <li>Home</li>
                <li>About</li>
                <li>Analyze</li>
            </ul>
        </div>
    </>
    )
}

export default NavBar