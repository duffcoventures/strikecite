import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ValidatorPage = () => {
  const [text, setText] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mode, setMode] = useState("text");
  const [jsonInput, setJsonInput] = useState("");
  const [reporters, setReporters] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    loadReporters();
  }, []);

  const loadReporters = async () => {
    try {
      const response = await axios.get(`${API}/reporters`);
      setReporters(response.data);
    } catch (err) {
      console.error("Failed to load reporters:", err);
    }
  };

  const validateText = async () => {
    if (!text.trim()) {
      setError("Please enter some text to validate");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const response = await axios.post(`${API}/validate-text`, { text });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Validation failed");
      console.error("Validation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const validateJSON = async () => {
    if (!jsonInput.trim()) {
      setError("Please enter LOOKUP_JSON data");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const lookupData = JSON.parse(jsonInput);
      const response = await axios.post(`${API}/validate-citations`, lookupData);
      setResults(response.data);
    } catch (err) {
      if (err instanceof SyntaxError) {
        setError("Invalid JSON format");
      } else {
        setError(err.response?.data?.detail || "Validation failed");
      }
      console.error("Validation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('text/') || file.name.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          setText(event.target.result);
        };
        reader.readAsText(file);
      } else {
        setError("Please drop a text file (.txt)");
      }
    }
  };

  const exportResults = () => {
    if (!results) return;
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'citation-validation-results.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const clearResults = () => {
    setResults(null);
    setError("");
    setText("");
    setJsonInput("");
  };

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case "high": return "text-green-700";
      case "medium": return "text-yellow-700";
      case "low": return "text-red-700";
      default: return "text-gray-700";
    }
  };

  const getStatusBadge = (verified) => {
    return verified 
      ? "bg-green-100 text-green-800 border-green-300" 
      : "bg-red-100 text-red-800 border-red-300";
  };

  return (
    <div className="validator-page">
      <div className="validator-header">
        <div className="validator-header-content">
          <h1 className="validator-title">Citation Validator</h1>
          <p className="validator-subtitle">
            Validate U.S. legal citations with our comprehensive database
          </p>
          <div className="dev-only validator-stats">
            <span className="stat-badge">
              {reporters.length} legal reporters loaded
            </span>
            <span className="stat-badge">
              Federal • Regional • State • Specialized
            </span>
          </div>
        </div>
      </div>

      <main className="validator-main">
        {/* Mode Selection */}
        <div className="mode-selection">
          <div className="mode-tabs">
            <button
              onClick={() => setMode("text")}
              className={`mode-tab ${mode === "text" ? "active" : ""}`}
            >
              <div className="mode-tab-icon">📄</div>
              <div className="mode-tab-content">
                <div className="mode-tab-title">Full Pipeline</div>
                <div className="mode-tab-desc">Complete text processing</div>
              </div>
            </button>
            <button
              onClick={() => setMode("json")}
              className={`mode-tab ${mode === "json" ? "active" : ""}`}
            >
              <div className="mode-tab-icon">⚙️</div>
              <div className="mode-tab-content">
                <div className="mode-tab-title">Validation Service</div>
                <div className="mode-tab-desc">Direct LOOKUP_JSON processing</div>
              </div>
            </button>
          </div>
          <div className="dev-only mode-description">
            {mode === "text" 
              ? "Layer B: CourtListener API integration → Strike Cite validation" 
              : "Layer A: Direct validation microservice for integration projects"}
          </div>
        </div>

        <div className="validator-content">
          {/* Input Section */}
          <div className="input-section">
            <div className="input-header">
              <h2 className="input-title">
                {mode === "text" ? "Document Input" : "LOOKUP_JSON Input"}
              </h2>
            </div>
            
            <div className="input-content">
              {mode === "text" ? (
                <div className="dropzone-container">
                  <div 
                    className={`dropzone ${dragActive ? "over" : ""}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    <textarea
                      value={text}
                      onChange={(e) => setText(e.target.value)}
                      placeholder="Paste legal text with citations here..."
                      className="text-input"
                    />
                    <div className="dropzone-overlay">
                      <div className="dropzone-icon">📎</div>
                      <p className="dropzone-text">Drop text file here</p>
                    </div>
                  </div>
                  <div className="input-hints">
                    <span>✓ Drag & drop text files</span>
                    <span>✓ Up to 64,000 characters</span>
                    <span>✓ Automatic citation extraction</span>
                    <div className="dev-only">
                      <span>Character count: {text.length}/64,000</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="json-input-container">
                  <textarea
                    value={jsonInput}
                    onChange={(e) => setJsonInput(e.target.value)}
                    placeholder='[{"citation": "410 U.S. 113", "normalized_citations": ["410 U.S. 113"], "start_index": 22, "end_index": 32, "status": 200, "clusters": [{"url": "https://..."}]}]'
                    className="json-input"
                  />
                  <div className="input-hints">
                    <span>✓ Direct LOOKUP_JSON processing</span>
                    <span>✓ Microservice validation</span>
                    <span>✓ Enhanced error detection</span>
                  </div>
                </div>
              )}

              <div className="input-actions">
                <button
                  onClick={mode === "text" ? validateText : validateJSON}
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? (
                    <>
                      <div className="spinner"></div>
                      Validating...
                    </>
                  ) : (
                    "Validate Citations"
                  )}
                </button>
                
                <button
                  onClick={clearResults}
                  className="btn btn-secondary"
                >
                  Clear
                </button>
              </div>

              {error && (
                <div className="error-message">
                  <div className="error-icon">⚠</div>
                  <span>{error}</span>
                </div>
              )}
            </div>
          </div>

          {/* Results Section */}
          <div className="results-section">
            <div className="results-header">
              <h2 className="results-title">Validation Results</h2>
              {results && (
                <button
                  onClick={exportResults}
                  className="btn btn-small"
                  title="Export results as JSON"
                >
                  Export JSON
                </button>
              )}
            </div>

            <div className="results-content">
              {!results ? (
                <div className="results-empty">
                  <div className="empty-icon">📋</div>
                  <p className="empty-title">No validation results yet</p>
                  <p className="empty-subtitle">Enter text or JSON above to validate citations</p>
                </div>
              ) : (
                <div className="results-data">
                  {/* Summary Stats */}
                  <div className="summary-stats">
                    <div className="stat-card">
                      <div className="stat-number">{results.summary.total}</div>
                      <div className="stat-label">TOTAL</div>
                    </div>
                    <div className="stat-card verified">
                      <div className="stat-number">{results.summary.verified}</div>
                      <div className="stat-label">VERIFIED</div>
                    </div>
                    <div className="stat-card invalid">
                      <div className="stat-number">{results.summary.unverified}</div>
                      <div className="stat-label">INVALID</div>
                    </div>
                    <div className={`stat-card confidence ${results.summary.confidence}`}>
                      <div className="stat-number">{results.summary.confidence.toUpperCase()}</div>
                      <div className="stat-label">CONFIDENCE</div>
                    </div>
                  </div>

                  {/* Citations List */}
                  <div className="citations-list">
                    {results.citations.map((citation, index) => (
                      <div key={index} className="citation-card">
                        <div className="citation-header">
                          <div className="citation-text">
                            <code className="citation-code">{citation.raw}</code>
                            {citation.normalized !== citation.raw && (
                              <div className="citation-normalized dev-only">
                                Normalized: <code>{citation.normalized}</code>
                              </div>
                            )}
                          </div>
                          <div className={`citation-status ${citation.verified ? 'verified' : 'invalid'}`}>
                            {citation.verified ? '✓ VERIFIED' : '⚠ INVALID'}
                          </div>
                        </div>
                        
                        <div className="citation-details">
                          <div className="citation-meta">
                            <span className="meta-item">
                              <strong>Reporter:</strong> {citation.reporter || "Unknown"}
                            </span>
                            <span className="meta-item dev-only">
                              <strong>Position:</strong> {citation.start_char}-{citation.end_char}
                            </span>
                          </div>
                          
                          {citation.note && (
                            <div className="citation-note">
                              <div className="note-icon">💡</div>
                              <span>{citation.note}</span>
                            </div>
                          )}
                          
                          {citation.source_url && (
                            <div className="citation-source">
                              <a 
                                href={citation.source_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="source-link"
                              >
                                View on CourtListener →
                              </a>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ValidatorPage;