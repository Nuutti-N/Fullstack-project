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
        <div className="section-divider"></div>
        <section className="features">
            <h2>Built for accuracy.</h2>
            <p className="features-sub">Every verification returns a structured verdict, confidence score, and recommend you can audit.</p>
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
        <div className="section-divider"></div>
        <section className="how-work">
            <h2>Three steps to certainty.</h2>
            <div className="works-grid">
                <div className="works-card">
                    <span className="work-number">01</span>
                    <h3>Paste content</h3>
                    <p>Drop in any text or code snippet you want to verify</p>
                </div>
                <div className="works-card">
                    <span className="work-number">02</span>
                    <h3>AI analyzes</h3>
                    <p>Our model cross-references claims, audits logic, and surfaces issues.</p>
                </div>
                <div className="works-card">
                    <span className="work-number">03</span>
                    <h3>Get a verdict</h3>
                    <p>A clear true/false/unclear verdict with confidence and reasoning.</p>
                </div>
            </div>
        </section>
        <div className="section-divider"></div>


    </>
    )
}

export default Home