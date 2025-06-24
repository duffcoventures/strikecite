import React, { useState } from "react";

const DocsPage = () => {
  const [activeTab, setActiveTab] = useState("overview");

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  return (
    <div className="docs-page">
      <div className="docs-container">
        <div className="docs-header">
          <h1>API Documentation</h1>
          <p className="docs-subtitle">
            Complete guide to integrating Strike Cite into your legal workflow
          </p>
        </div>

        <div className="docs-nav">
          <button 
            className={`docs-tab ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            Overview
          </button>
          <button 
            className={`docs-tab ${activeTab === "layera" ? "active" : ""}`}
            onClick={() => setActiveTab("layera")}
          >
            Layer A API
          </button>
          <button 
            className={`docs-tab ${activeTab === "layerb" ? "active" : ""}`}
            onClick={() => setActiveTab("layerb")}
          >
            Layer B API
          </button>
          <button 
            className={`docs-tab ${activeTab === "examples" ? "active" : ""}`}
            onClick={() => setActiveTab("examples")}
          >
            Examples
          </button>
        </div>

        <div className="docs-content">
          {activeTab === "overview" && (
            <div className="docs-section">
              <h2>API Overview</h2>
              <p>
                Strike Cite provides a RESTful API with two main validation endpoints 
                designed for different integration scenarios.
              </p>
              
              <div className="api-info">
                <div className="info-item">
                  <strong>Base URL:</strong> <code>{BACKEND_URL}/api</code>
                </div>
                <div className="info-item">
                  <strong>Content-Type:</strong> <code>application/json</code>
                </div>
                <div className="info-item">
                  <strong>Rate Limits:</strong> None currently applied
                </div>
              </div>

              <h3>Available Endpoints</h3>
              <div className="endpoints-list">
                <div className="endpoint-item">
                  <div className="endpoint-method">GET</div>
                  <div className="endpoint-path">/health</div>
                  <div className="endpoint-desc">System health and reporter count</div>
                </div>
                <div className="endpoint-item">
                  <div className="endpoint-method">GET</div>
                  <div className="endpoint-path">/reporters</div>
                  <div className="endpoint-desc">List all available legal reporters</div>
                </div>
                <div className="endpoint-item">
                  <div className="endpoint-method">POST</div>
                  <div className="endpoint-path">/validate-citations</div>
                  <div className="endpoint-desc">Layer A: Validate LOOKUP_JSON data</div>
                </div>
                <div className="endpoint-item">
                  <div className="endpoint-method">POST</div>
                  <div className="endpoint-path">/validate-text</div>
                  <div className="endpoint-desc">Layer B: Complete text processing pipeline</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "layera" && (
            <div className="docs-section">
              <h2>Layer A: Citation Validation Microservice</h2>
              <p>
                Validates LOOKUP_JSON data from CourtListener API. Perfect for integration 
                into existing workflows where you already have citation extraction.
              </p>

              <div className="api-endpoint">
                <div className="endpoint-header">
                  <span className="method">POST</span>
                  <span className="path">/validate-citations</span>
                </div>
                
                <h4>Request Body</h4>
                <pre className="code-block">
{`[
  {
    "citation": "410 U.S. 113",
    "normalized_citations": ["410 U.S. 113"],
    "start_index": 22,
    "end_index": 32,
    "status": 200,
    "clusters": [{"url": "https://..."}]
  }
]`}
                </pre>

                <h4>Response</h4>
                <pre className="code-block">
{`{
  "citations": [
    {
      "raw": "410 U.S. 113",
      "normalized": "410 U.S. 113",
      "reporter": "U.S.",
      "verified": true,
      "source_url": "https://...",
      "note": "",
      "start_char": 22,
      "end_char": 32
    }
  ],
  "summary": {
    "total": 1,
    "verified": 1,
    "unverified": 0,
    "confidence": "high"
  }
}`}
                </pre>
              </div>
            </div>
          )}

          {activeTab === "layerb" && (
            <div className="docs-section">
              <h2>Layer B: Complete Text Processing Pipeline</h2>
              <p>
                End-to-end processing that extracts citations from text using CourtListener API 
                and validates them through Strike Cite.
              </p>

              <div className="api-endpoint">
                <div className="endpoint-header">
                  <span className="method">POST</span>
                  <span className="path">/validate-text</span>
                </div>
                
                <h4>Request Body</h4>
                <pre className="code-block">
{`{
  "text": "In Roe v. Wade, 410 U.S. 113 (1973), the Court ruled..."
}`}
                </pre>

                <h4>Response</h4>
                <pre className="code-block">
{`{
  "citations": [
    {
      "raw": "410 U.S. 113",
      "normalized": "410 U.S. 113",
      "reporter": "U.S.",
      "verified": true,
      "source_url": null,
      "note": "",
      "start_char": 18,
      "end_char": 30
    }
  ],
  "summary": {
    "total": 1,
    "verified": 1,
    "unverified": 0,
    "confidence": "high"
  }
}`}
                </pre>
              </div>
            </div>
          )}

          {activeTab === "examples" && (
            <div className="docs-section">
              <h2>Integration Examples</h2>
              
              <h3>Python Example</h3>
              <pre className="code-block">
{`import requests

# Layer B: Text validation
response = requests.post(
    "${BACKEND_URL}/api/validate-text",
    json={"text": "Your legal document text here..."},
    headers={"Content-Type": "application/json"}
)
result = response.json()

# Layer A: Direct citation validation
lookup_data = [
    {
        "citation": "410 U.S. 113",
        "normalized_citations": ["410 U.S. 113"],
        "start_index": 0,
        "end_index": 11,
        "status": 200,
        "clusters": []
    }
]

response = requests.post(
    "${BACKEND_URL}/api/validate-citations",
    json=lookup_data,
    headers={"Content-Type": "application/json"}
)
result = response.json()`}
              </pre>

              <h3>JavaScript Example</h3>
              <pre className="code-block">
{`// Using fetch API
const validateText = async (text) => {
  const response = await fetch('${BACKEND_URL}/api/validate-text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return await response.json();
};

// Using axios
import axios from 'axios';

const validateCitations = async (lookupData) => {
  const response = await axios.post(
    '${BACKEND_URL}/api/validate-citations',
    lookupData,
    { headers: { 'Content-Type': 'application/json' }}
  );
  return response.data;
};`}
              </pre>

              <h3>cURL Examples</h3>
              <pre className="code-block">
{`# Text validation
curl -X POST "${BACKEND_URL}/api/validate-text" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "In Brown v. Board, 347 U.S. 483 (1954)..."}'

# Citation validation
curl -X POST "${BACKEND_URL}/api/validate-citations" \\
  -H "Content-Type: application/json" \\
  -d '[{"citation":"410 U.S. 113","status":200,"clusters":[]}]'`}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocsPage;