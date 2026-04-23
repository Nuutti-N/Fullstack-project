import { useState } from "react"
import api from "../api/client"
import { useNavigate, Link } from "react-router-dom"

function Signup() {
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        const response = await api.post("/signup", { username, password })

        navigate("/login")

    }
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />
            <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <button type="submit">Sign up</button>
            <p>Already have an account?</p>
            <Link to="/login" className="auth-link">Log in</Link>
        </form>

    )
}

export default Signup