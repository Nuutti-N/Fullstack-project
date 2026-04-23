import { useState } from "react"
import api from "../api/client"
import { useNavigate } from "react-router-dom"
import "../components/Login/login.css"

function Login() {
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [showPassword, setShowPassword] = useState("")
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        const data = new URLSearchParams()
        data.append("username", username)
        data.append("password", password)
        const response = await api.post("/login", data)
        localStorage.setItem("token", response.data.access_token)
        console.log(response.data)
        navigate("/analyze")
    }
    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="title">Welcome back</label>
            <label htmlFor="subtitle">Log in to verify account</label>


            <label htmlFor="username">Username</label>
            <input
                type="text"
                placeholder="username"
                className="username-input"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />
            <label htmlFor="password">Password</label>
            <button type="button" className="forgot-link">Forgot password</button>
            <input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                className="password-input"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}></button>
            <button type="submit">Log in</button>
        </form>
    )
}

export default Login

