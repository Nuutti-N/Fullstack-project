import { useState } from "react"
import api from "../api/client"
import { useNavigate } from "react-router-dom"

function Signup() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    return (
        <form>
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
        </form>

    )
}

export default Signup