import { useState } from "react"
import api from "../api/client"
import { useNavigate, Link } from "react-router-dom"
import "../components/Auth/login.css"
import { Eye, EyeOff, ArrowRight } from "lucide-react"


function Login() {
    const navigate = useNavigate()
    const [error, setError] = useState("")
    const [username, setUsername] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        try {
            setError("")
            const data = new URLSearchParams()
            data.append("username", username)
            data.append("password", password)
            const response = await api.post("/login", data)
            localStorage.setItem("token", response.data.access_token)
            navigate("/analyze")
        }
        catch (err) {
            setError("wrong username or password")
        }
    }
    return (
        <div className="auth-page">
            <form className="auth-form" onSubmit={handleSubmit}>
                <header className="auth-header">
                    <h1 className="auth-title">Welcome back</h1>
                    <p className="auth-subtitle">Log in to verify your account</p>
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
                <div>
                    <div className="password-row">
                        <label htmlFor="password">Password</label>
                        <button type="button" className="forgot-link">Forgot password</button>
                    </div>
                    <div className="password-wrapper">
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
                            className="hide-button"
                            onClick={() => setShowPassword(!showPassword)}>{showPassword ? <EyeOff /> : <Eye />}</button>
                    </div>
                </div>
                {
                    error &&
                    <p className="auth-error">{error}</p>
                }
                <button type="submit" className="auth-submit">Log in
                    <ArrowRight />
                </button>
                {/* divider */}
                <div className="auth-divider">
                    <div className="line" />
                    <span> or continue with</span>
                    <div className="line" />
                </div>

                <div className="auth-toggle">
                    <p className="auth-no">Don't have an account?</p>
                    <Link to="/signup" className="auth-link">Sign up</Link>
                </div>
            </form >
        </div >
    )
}

export default Login

