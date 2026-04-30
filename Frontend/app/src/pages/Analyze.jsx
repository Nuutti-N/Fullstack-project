import { useState, useEffect } from "react"
import api from "../api/client"
import "./analyze.css"
import { Loader2, Sparkles, History } from "lucide-react"


function Analyze() {
    const [type, setType] = useState("text")
    const [text, setText] = useState("")
    const [results, setResults] = useState(null)
    const [history, setHistory] = useState([])
    const [showHistory, setShowHistory] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    async function handleSubmit(e) {
        e.preventDefault()
        setLoading(true)
        try {
            setError("")
            const response = await api.post("/analyze", JSON.stringify(text), { headers: { "Content-Type": "application/json" } })
            setResults(response.data)
        } catch (err) {
            setError("Something went wrong. Try again.")
        } finally {
            setLoading(false)
        }
    }
    useEffect(() => {
        async function loadhistory() {
            const response = await api.get("/history", { params: { limit: 100 } })
            setHistory(response.data)
        }
        loadhistory()
    }, [])

    return (
        <div className="analyze-page">
            <div className="analyze-text">
                <h1 className="analyze-title">Analyze.</h1>
                <p className="analyze-subtitle">Paste any text or code. Get an AI verdict in seconds</p>
            </div>
            {!showHistory &&
                <form className="analyze-card" onSubmit={handleSubmit}>
                    <button type="button" onClick={() => setType("text")}
                        className={"Analyze-type-btn " + (type === "text" ? "type-active" : "")}>
                        Text
                    </button>
                    <button type="button" onClick={() => setType("code")}
                        className={"Analyze-type-btn " + (type === "code" ? "type-active" : "")}>
                        Code
                    </button>
                    <button type="button" onClick={() => setShowHistory(true)}>
                        <History />
                        {history.length > 0 && (
                            <span >{history.length}</span>
                        )}
                    </button>
                    <textarea
                        placeholder={type === "code" ? "Paste code to audit..." : "Paste a claim, article or post to fact-check..."}
                        className="analyze-input"
                        value={text}
                        onChange={e => setText(e.target.value)}
                        maxLength={2000}
                    />
                    <div className="analyze-footer">
                        <span className="analyze-length">{text.length}/2000</span>
                        <button className="analyze-btn" type="submit" disabled={loading}><Sparkles className="analyze-sparkles" />{loading ? <Loader2 /> : "Analyze"} </button>
                    </div>
                </form>}
            {showHistory &&
                history.map(item => (<div key={item.id}>  <p>{item.score}</p>
                    <p>{item.verdict}</p>
                    <p>{item.risks}</p>
                    <p>{item.pros}</p>
                    <p>{item.recommend}</p></div>))}
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