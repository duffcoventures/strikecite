import React from "react";
import { Link, useLocation } from "react-router-dom";

const Header = ({ devMode, setDevMode }) => {
  const location = useLocation();

  return (
    <header className="topnav">
      <Link to="/" className="logo">
        ⚖️ Strike Cite
      </Link>
      <nav className="nav-links">
        <Link 
          to="/" 
          className={location.pathname === "/" ? "active" : ""}
        >
          Home
        </Link>
        <Link 
          to="/app" 
          className={location.pathname === "/app" ? "active" : ""}
        >
          Validate
        </Link>
        <Link 
          to="/docs" 
          className={location.pathname === "/docs" ? "active" : ""}
        >
          API Docs
        </Link>
        <Link 
          to="/about" 
          className={location.pathname === "/about" ? "active" : ""}
        >
          About
        </Link>
        <div className="dev-toggle-container">
          <button 
            className={`dev-toggle ${devMode ? 'active' : ''}`}
            onClick={() => setDevMode(!devMode)}
            title="Toggle Developer Mode"
          >
            DEV
          </button>
        </div>
      </nav>
    </header>
  );
};

export default Header;