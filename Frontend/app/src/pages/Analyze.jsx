import { useState } from "react"
import api from "../api/client"
import "./analyze.css"
import { Loader2, Sparkles } from "lucide-react"


function Analyze() {
    const [type, setType] = useState("text")
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


    return (
        <div className="analyze-page">
            {/* <h1 className="analyze-title">Analyze</h1>
            <p className="analyze-title">Paste any text or code. Get an AI verdict in seconds</p> */}
            <form className="analyze-card" onSubmit={handleSubmit}>
                <button type="button" onClick={() => setType("text")}
                    className={type === "text" ? "type-active" : ""}>
                    Text
                </button>
                <button type="button" onClick={() => setType("code")}
                    className={type === "code" ? "type-active" : ""}>
                    Code
                </button>
                <textarea
                    placeholder={type === "code" ? "Paste code to audit..." : "Paste a claim, article or post to fact-check..."}
                    className="analyze-input"
                    value={text}
                    onChange={e => setText(e.target.value)}
                    maxLength={8000}
                />
                <div className="analyze-footer">
                    <span >{text.length}/8000</span>
                    <button className="analyze-btn" type="submit" disabled={loading}><Sparkles className="analyze-sparkles" />{loading ? <Loader2 /> : "Analyze"} </button>
                </div>
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
        </div>)
}


export default Analyze