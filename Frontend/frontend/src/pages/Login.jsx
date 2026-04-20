import { useState } from "react"

function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        console.log(username, password)
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

