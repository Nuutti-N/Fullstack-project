import { useState } from "react"
import api from "../api/client"
import { useNavigate, useSearchParams, Link } from "react-router-dom"
import "../components/Login/login.css"
import { Eye, EyeOff } from "lucide-react"


function Login() {
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()
    const [username, setUsername] = useState("")
    const [showPassword, setShowPassword] = useState(false)
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
        <div className="auth-page">
            <form className="auth-card" onSubmit={handleSubmit}>
                <header className="auth-header">
                    <h1>Welcome back</h1>
                    <p>Log in to verify your account</p>
                </header>
                <div className="username-row">
                    <label htmlFor="username">Username</label>
                </div>
                <input
                    id="username"
                    type="text"
                    placeholder="username"
                    className="username-input"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
                <div className="password-row">
                    <label htmlFor="password">Password</label>
                    <button type="button" className="forgot.link">Forgot password</button>
                </div>
                <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    className="password-input"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    minLength={8}
                />
                <button
                    type="button"
                    className="password-toggle" onClick={() => setShowPassword(!showPassword)}>{showPassword ? <EyeOff /> : <Eye />}</button>
                <button type="submit">Log in</button>

                <p>Don't have an account?</p>
                <Link to="/signup" className="auth-link">Sign up</Link>
            </form>
        </div>
    )
}

export default Login

