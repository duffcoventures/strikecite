import React from "react";
import { Link, useLocation } from "react-router-dom";

const Header = () => {
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
          Validate Citations
        </Link>
        <Link 
          to="/about" 
          className={location.pathname === "/about" ? "active" : ""}
        >
          About
        </Link>
      </nav>
    </header>
  );
};

export default Header;