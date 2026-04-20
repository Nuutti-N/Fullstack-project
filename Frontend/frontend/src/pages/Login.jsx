import { useState } from "react"
import api from "../api/client"
import { useNavigate } from "react-router-dom"


function Login() {
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        const data = new URLSearchParams()
        data.append("username", username)
        data.append("password", password)
        const response = await api.post("/login", data)
        localStorage.setItem("token", response.data.access_token)
        console.log(response.data)
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
            <button type="submit">Log in</button>
        </form>
    )
}

export default Login

