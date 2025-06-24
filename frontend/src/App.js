import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import HomePage from "./components/HomePage";
import ValidatorPage from "./components/ValidatorPage";
import AboutPage from "./components/AboutPage";
import DocsPage from "./components/DocsPage";

function App() {
  const [devMode, setDevMode] = useState(false);

  return (
    <div className={`App ${devMode ? 'dev' : ''}`}>
      <Router>
        <Header devMode={devMode} setDevMode={setDevMode} />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/app" element={<ValidatorPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/docs" element={<DocsPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;