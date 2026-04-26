import { useState } from "react"
import api from "../api/client"
import { useNavigate, Link } from "react-router-dom"
import { Eye, EyeOff, ArrowRight } from "lucide-react"

function Signup() {
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        try {
            const response = await api.post("/signup", { username, password })
            navigate("/login")
        }
        catch (err) {
            setError("username or password invalid")
        }

    }
    return (
        <div className="auth-page">
            <form className="auth-form" onSubmit={handleSubmit}>
                <header className="auth-header">
                    <h1 className="auth-title">Create  account</h1>
                    <p className="auth-subtitle">Start fact-checking AI today</p>
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
                </div>
                <div className="password-wrapper">
                    <input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={password}
                        className="password-input"
                        onChange={e => setPassword(e.target.value)}
                        minLength={8}
                    />
                    <button
                        type="button"
                        className="hide-button"
                        onClick={() => setShowPassword(!showPassword)}
                    >{showPassword ? <EyeOff /> : <Eye />}</button>
                </div>
                {
                    error && <p className="auth-error">{error}</p>
                }
                <button type="submit" className="auth-submit">Sign up
                    <ArrowRight />
                </button>
                <div className="auth-toggle">
                    <p>Already have an account?</p>
                    <Link to="/login" className="auth-link">Log in</Link>
                </div>
            </form>
        </div>

    )
}

export default Signup