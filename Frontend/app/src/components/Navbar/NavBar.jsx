
import { useNavigate, useLocation } from "react-router-dom"
import { useState, useEffect } from "react"
import api from "../../api/client"
import "./NavBar.css"

function NavBar() {
    const location = useLocation()
    if (location.pathname === "/login" || location.pathname === "/signup") return null
    const [user, setUser] = useState(null)
    const [Loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const navigate = useNavigate()
    useEffect(() => {
        async function loadUser() {
            setLoading(true)
            try {
                setError("")
                const response = await api.get("/your")
                setUser(response.data)
            }
            catch (err) {
                setError("Could not load user.")
            }
            finally {
                setLoading(false)
            }
        }
        loadUser()
    }, [])
    function handleLogout() {
        localStorage.removeItem('token')
        navigate("/login")
    }



    return (<>
        {user &&
            <span>How can I help you, {user.username}</span>}
        <button onClick={handleLogout}>Log out</button>
        <header className="header">
            <div className="nav-left">
                <a href="/">logo</a>
            </div>
            <div className="nav-middle">
                <a href="/">Features</a>
                <a href="/">How it works</a>
            </div>
            <div className="nav-right">
                <a href="/">Log in</a>
                <a href="/">Get started</a>
            </div>
        </header>
    </>
    )
}

export default NavBar