import { useState, useEffect } from "react"
import api from "../api/client"
import "./analyze.css"
import { Loader2, Sparkles, History, X } from "lucide-react"


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
    async function handleDelete(id) {
        const response = await api.delete(`/delete_history/${id}`)
        setHistory(history.filter(item => item.id !== id))
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
            </form>
            {showHistory &&
                <div onClick={() => setShowHistory(false)} className="overlay-panel"></div>}
            <div className={showHistory ? "history-panel open" : "history-panel"}>
                <div className="history-navbar">
                    <History className="history-icon" />
                    <h2 className="history-title"> History  <span className="history-length">({history.length})</span>
                    </h2>
                    <button className="x-btn" onClick={() => setShowHistory(false)}>
                        <X className="x-panel" />
                    </button>
                </div>
                <div className="section-divider"></div>
                {history.map(item => (<div className="history-item" key={item.id}>
                    <p>{item.claim}</p>
                    <button onClick={() => handleDelete(item.id)}>Delete</button></div>
                ))}
                {history.length === 0 && (
                    <div className="history-sub">
                        No analyses yet. Your history will appear here.
                    </div>
                )}
            </div>
            {error &&
                <p style={{ color: "red" }}>{error}</p>}
            {results && (
                <div>
                    {results.risks.map((risk, index) => (
                        <p key={index}>{risk}</p>))}
                    {results.pros.map((pros, index) => (
                        <p key={index}>{pros}</p>
                    ))}
                    <p>Score: {results.score}</p>
                    <p>Verdict: {results.verdict}</p>
                    <p>pros: {results.pros}</p>
                    <p>recommend: {results.recommend}</p>
                </div>
            )}
        </div>)
}

export default Analyze