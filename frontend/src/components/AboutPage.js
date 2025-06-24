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
            <h2>How It Works</h2>
            <div className="architecture-grid">
              <div className="layer-card">
                <h3>Comprehensive Database</h3>
                <p>
                  Our system validates citations against a comprehensive database of 
                  8.9 million U.S. legal opinions, updated daily with new federal 
                  and state court decisions.
                </p>
                <ul>
                  <li>149+ comprehensive legal reporters</li>
                  <li>Federal, Regional, State, and Specialized courts</li>
                  <li>Advanced typo detection and correction suggestions</li>
                  <li>Real-time validation against authoritative sources</li>
                </ul>
              </div>
              
              <div className="layer-card">
                <h3>Smart Validation</h3>
                <p>
                  Our intelligent system automatically extracts citations from 
                  your documents and validates them against our comprehensive 
                  legal database in seconds.
                </p>
                <ul>
                  <li>Automatic citation extraction from PDFs and text</li>
                  <li>Instant validation and verification</li>
                  <li>Drag-and-drop file processing</li>
                  <li>Professional validation reports</li>
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
            <h2>Why Strike Cite?</h2>
            <p>
              In an era where AI-generated legal content can include fabricated citations, 
              professional verification has become essential. Strike Cite provides the 
              confidence you need to file with certainty.
            </p>
            <ul>
              <li><strong>Prevent Sanctions:</strong> Avoid embarrassing citation errors that could lead to court sanctions</li>
              <li><strong>Professional Competence:</strong> Maintain the highest standards of legal practice</li>
              <li><strong>Challenge Opponents:</strong> Quickly verify opposing counsel's citations</li>
              <li><strong>Save Time:</strong> Instant validation instead of manual checking</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;