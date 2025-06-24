import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Professional Legal Citation Validation
          </h1>
          <p className="hero-subtitle">
            Validate U.S. legal citations with precision using our comprehensive database of 149+ court reporters and advanced error detection.
          </p>
          <div className="hero-actions">
            <Link to="/app" className="btn btn-primary">
              Start Validating
            </Link>
            <Link to="/docs" className="btn btn-secondary">
              View API Docs
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <div className="citation-preview">
            <div className="citation-example">
              <span className="citation-text verified">410 U.S. 113</span>
              <span className="status-badge verified">✓ VERIFIED</span>
            </div>
            <div className="citation-example">
              <span className="citation-text invalid">123 F3rd 456</span>
              <span className="status-badge invalid">⚠ F.3d suggested</span>
            </div>
            <div className="citation-example">
              <span className="citation-text verified">999 So. 2d 123</span>
              <span className="status-badge verified">✓ VERIFIED</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="features-container">
          <h2 className="section-title">Two-Layer Validation Architecture</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Layer A: Core Validation</h3>
              <p>
                Reusable microservice that validates LOOKUP_JSON from CourtListener API. 
                Perfect for integration into existing legal tech workflows.
              </p>
              <ul>
                <li>Processes any citation data format</li>
                <li>Advanced error detection</li>
                <li>Typo identification & suggestions</li>
                <li>Reporter recognition</li>
              </ul>
            </div>
            <div className="feature-card">
              <h3>Layer B: Complete Pipeline</h3>
              <div className="feature-icon">⚡</div>
              <p>
                End-to-end text processing with automatic citation extraction 
                and validation. Drop in your legal documents and get instant results.
              </p>
              <ul>
                <li>Automatic citation extraction</li>
                <li>CourtListener API integration</li>
                <li>Drag & drop file support</li>
                <li>Bulk document processing</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats">
        <div className="stats-container">
          <div className="stat-item">
            <div className="stat-number">149+</div>
            <div className="stat-label">Legal Reporters</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">Federal</div>
            <div className="stat-label">Supreme Court to District</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">Regional</div>
            <div className="stat-label">All Circuit Reporters</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">State</div>
            <div className="stat-label">Comprehensive Coverage</div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="cta-content">
          <h2>Ready to validate your legal citations?</h2>
          <p>Join legal professionals who trust Strike Cite for accurate citation validation.</p>
          <Link to="/app" className="btn btn-primary btn-large">
            Try Strike Cite Now
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;