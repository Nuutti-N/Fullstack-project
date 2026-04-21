import { useState } from "react"
import api from "../api/client"



function Analyze() {
    const [text, setText] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
    }


    return <form onSubmit={handleSubmit}>
        <textarea>
            value={text}
            onChange={e => setText(e.target.value)}

        </textarea>
        <button type="submit">Analyze</button>
    </form>
}


export default Analyze