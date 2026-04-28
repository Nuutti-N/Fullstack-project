import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import "./home.css"

function Home() {


    return (<>
        <div className="hero">
            <a className="hero-badge" href="/" >AI-powered truth detection</a>
            <h1>Verify what's <em className="hero-true">true</em>.<br />
                In text. In code.</h1>
            <Link to="/signup" className="hero-verify">Start verifying free <ArrowRight /> </Link>



        </div>

    </>
    )
}

export default Home