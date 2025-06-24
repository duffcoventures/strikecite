import React from "react";

const AboutPage = () => {
  return (
    <div className="about-page">
      <div className="about-container">
        <div className="about-header">
          <h1>About Strike Cite</h1>
          <p className="about-subtitle">
            Professional legal citation validation for the modern legal workflow
          </p>
        </div>

        <div className="about-content">
          <section className="about-section">
            <h2>Our Mission</h2>
            <p>
              Strike Cite provides accurate, reliable validation of U.S. legal citations 
              through comprehensive reporter databases and intelligent error detection. 
              We help legal professionals ensure citation accuracy and maintain 
              professional standards in legal documents.
            </p>
          </section>

          <section className="about-section">
            <h2>Two-Layer Architecture</h2>
            <div className="architecture-grid">
              <div className="layer-card">
                <h3>Layer A: Validation Microservice</h3>
                <p>
                  Our core validation engine processes LOOKUP_JSON data from 
                  CourtListener API, providing detailed analysis of citation 
                  accuracy, reporter recognition, and error detection.
                </p>
                <ul>
                  <li>149+ comprehensive legal reporters</li>
                  <li>Federal, Regional, State, and Specialized courts</li>
                  <li>Advanced typo detection and correction suggestions</li>
                  <li>Confidence scoring and detailed error reporting</li>
                </ul>
              </div>
              
              <div className="layer-card">
                <h3>Layer B: Complete Pipeline</h3>
                <p>
                  End-to-end text processing that automatically extracts citations 
                  from legal documents and validates them through our comprehensive 
                  reporter database.
                </p>
                <ul>
                  <li>Automatic citation extraction from text</li>
                  <li>CourtListener API integration</li>
                  <li>Drag-and-drop file processing</li>
                  <li>Bulk document validation</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Coverage</h2>
            <div className="coverage-grid">
              <div className="coverage-item">
                <h4>Federal Courts</h4>
                <p>Supreme Court, Courts of Appeals, District Courts, and specialized federal tribunals</p>
              </div>
              <div className="coverage-item">
                <h4>Regional Reporters</h4>
                <p>All West Regional Reporters including Atlantic, Pacific, South Eastern, and more</p>
              </div>
              <div className="coverage-item">
                <h4>State Courts</h4>
                <p>Official state reporters and appellate court decisions across all 50 states</p>
              </div>
              <div className="coverage-item">
                <h4>Specialized Courts</h4>
                <p>Tax Court, Bankruptcy, Military Appeals, Veterans Affairs, and International Trade</p>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Technology</h2>
            <p>
              Built with modern web technologies for reliability and performance:
            </p>
            <ul>
              <li><strong>Backend:</strong> FastAPI with MongoDB for high-performance data processing</li>
              <li><strong>Frontend:</strong> React with responsive design for all devices</li>
              <li><strong>Data:</strong> Comprehensive legal reporter database with regular updates</li>
              <li><strong>Integration:</strong> RESTful API for easy integration into existing workflows</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;