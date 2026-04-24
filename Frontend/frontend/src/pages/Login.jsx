import { useState } from "react"
import api from "../api/client"
import { useNavigate, useSearchParams, Link } from "react-router-dom"
import "../components/Auth/login.css"
import { Eye, EyeOff, ArrowRight } from "lucide-react"


function Login() {
    const navigate = useNavigate()
    const [error, setError] = useState("")
    const [searchParams] = useSearchParams()
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
                {/* Social button */}
                <div className="social-buttons">
                    <button className="social-btn">
                        <svg viewBox="0 0 24 24">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                        </svg>
                        Google
                    </button>
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

