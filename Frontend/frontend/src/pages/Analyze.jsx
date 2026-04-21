import { useState } from "react"
import api from "../api/client"



function Analyze() {
    const [text, setText] = useState("")
    const [results, setResults] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        setLoading(true)
        try {
            setError("")
            const response = await api.post("/analyze", null, { params: { text } })
            setResults(response.data)
        } catch (err) {
            setError("Something went wrong. Try again.")
        } finally {
            setLoading(false)
        }
    }


    return (<> <form onSubmit={handleSubmit}>
        <textarea
            value={text}
            onChange={e => setText(e.target.value)}

        />
        <button type="submit" disabled={loading}>{loading ? "Analyzing..." : "Analyze"}</button>
    </form>
        {error &&
            <p style={{ color: "red" }}>{error}</p>}
        {results && (
            <div>
                <p>Score: {results.score}</p>
                <p>Verdict: {results.verdict}</p>
                <p>risks: {results.risks}</p>
                <p>pros: {results.pros}</p>
                <p>recommend: {results.recommend}</p>
            </div>
        )}

    </>)
}


export default Analyze