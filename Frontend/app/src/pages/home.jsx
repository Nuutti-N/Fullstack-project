import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import "./home.css"

function Home() {


    return (<>
        <div className="hero">
            <a className="hero-badge" href="/" >AI-powered truth detection</a>
            <h1>Verify what's <em className="hero-true">true</em>.<br />
                In text. In code.</h1>
            <p> App uses advanced AI to fact-check claims, audit code, <br />
                and surface the signals you need to trust what you read</p>
            <div className="hero-actions">
                <Link to="/signup" className="hero-verify" >Start verifying free <ArrowRight /> </Link>
                <Link to="/" className="hero-work">See how it works</Link>
            </div>
        </div>
        <section className="features">
            <h2>Built for accuracy.</h2>
            <p>Every verification returns a structure verdict, confidence score, and recommend you can audit.</p>
            <div className="features-grid">
                <div className="features-card">
                    <h3>Text fact-checking</h3>
                    <p>Detect misinformation, logical, fallacies, and unsupported claims in articles, posts, and reports.</p>
                </div>
                <div className="features-card">
                    <h3>Code auditing</h3>
                    <p>Identify bugs, security issues, and false claims in code comments or documentation.</p>
                </div>
                <div className="features-card">
                    <h3>Confidence scoring</h3>
                    <p>Every verdict comes with a 0-100 confidence score so you know how certain the model is</p>
                </div>
            </div>
        </section>


    </>
    )
}

export default Home