import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Analysis from "./pages/Analysis";
import Details from "./pages/Details";
import About from "./pages/About";

function App() {
  return (
    <Router>
      <Header />
      <div className="App">  
        <div className="routes-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analysis" element={<Analysis />} />
            <Route path="/analysis/details" element={<Details />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
      <Footer />
    </Router>
  );
}

export default App;