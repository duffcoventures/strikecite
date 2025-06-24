import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ValidatorPage = () => {
  const [text, setText] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploadMethod, setUploadMethod] = useState("pdf"); // "pdf", "text", "json"
  const [jsonInput, setJsonInput] = useState("");
  const [reporters, setReporters] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

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

  const validatePDF = async (file) => {
    setLoading(true);
    setError("");
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${API}/validate-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "PDF validation failed");
      console.error("PDF validation error:", err);
    } finally {
      setLoading(false);
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
      setError("Please enter citation data");
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
      handleFileUpload(file);
    }
  };

  const handleFileUpload = (file) => {
    if (file.type === 'application/pdf') {
      setUploadedFile(file);
      setUploadMethod("pdf");
      validatePDF(file);
    } else if (file.type.startsWith('text/') || file.name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
        setUploadMethod("text");
      };
      reader.readAsText(file);
    } else {
      setError("Please upload a PDF document or text file");
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const exportResults = () => {
    if (!results) return;
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'citation-validation-report.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const clearAll = () => {
    setResults(null);
    setError("");
    setText("");
    setJsonInput("");
    setUploadedFile(null);
  };

  const getValidationSummary = () => {
    if (!results) return null;
    
    const { total, verified, unverified } = results.summary;
    const hasIssues = unverified > 0;
    
    return (
      <div className={`validation-summary ${hasIssues ? 'has-issues' : 'all-good'}`}>
        <div className="summary-icon">
          {hasIssues ? '⚠️' : '✅'}
        </div>
        <div className="summary-text">
          {hasIssues ? (
            <>
              <strong>Citations Need Review</strong>
              <p>{unverified} of {total} citations have issues that need your attention</p>
            </>
          ) : (
            <>
              <strong>All Citations Valid</strong>
              <p>All {total} citations have been verified in legal databases</p>
            </>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="validator-page-legal">
      <div className="validator-header-legal">
        <div className="validator-header-content">
          <h1 className="validator-title-legal">Citation Validator</h1>
          <p className="validator-subtitle-legal">
            Upload your legal brief or paste text to instantly validate all citations
          </p>
        </div>
      </div>

      <main className="validator-main-legal">
        {/* Upload Methods */}
        <div className="upload-methods">
          <button
            onClick={() => setUploadMethod("pdf")}
            className={`method-btn ${uploadMethod === "pdf" ? "active" : ""}`}
          >
            <div className="method-icon">📄</div>
            <div className="method-text">
              <div className="method-title">Upload PDF Brief</div>
              <div className="method-desc">Most common - upload your legal documents</div>
            </div>
          </button>
          <button
            onClick={() => setUploadMethod("text")}
            className={`method-btn ${uploadMethod === "text" ? "active" : ""}`}
          >
            <div className="method-icon">📝</div>
            <div className="method-text">
              <div className="method-title">Paste Text</div>
              <div className="method-desc">Copy and paste document text directly</div>
            </div>
          </button>
          <div className="dev-only">
            <button
              onClick={() => setUploadMethod("json")}
              className={`method-btn ${uploadMethod === "json" ? "active" : ""}`}
            >
              <div className="method-icon">⚙️</div>
              <div className="method-text">
                <div className="method-title">API Integration</div>
                <div className="method-desc">For developers - direct citation data</div>
              </div>
            </button>
          </div>
        </div>

        <div className="validator-content-legal">
          {/* Input Section */}
          <div className="input-section-legal">
            {uploadMethod === "pdf" && (
              <div className="pdf-upload-area">
                <div 
                  className={`dropzone-legal ${dragActive ? "over" : ""}`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <div className="dropzone-content">
                    <div className="dropzone-icon">📄</div>
                    <h3>Drag and drop your PDF brief here</h3>
                    <p>Or click to browse and select your file</p>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileInputChange}
                      className="file-input-hidden"
                      id="pdf-upload"
                    />
                    <label htmlFor="pdf-upload" className="btn btn-upload">
                      Choose PDF File
                    </label>
                  </div>
                  
                  {uploadedFile && (
                    <div className="uploaded-file-info">
                      <div className="file-icon">📄</div>
                      <div className="file-details">
                        <div className="file-name">{uploadedFile.name}</div>
                        <div className="file-size">
                          {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                <div className="upload-hints">
                  <span>✓ Supports legal briefs, motions, and court documents</span>
                  <span>✓ Secure processing - files are not stored</span>
                  <span>✓ Instant results in under 30 seconds</span>
                </div>
              </div>
            )}

            {uploadMethod === "text" && (
              <div className="text-upload-area">
                <div className="text-input-container">
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste your legal document text here. Include the full text with citations to validate..."
                    className="text-input-legal"
                  />
                  <div className="text-counter">
                    {text.length.toLocaleString()} characters
                  </div>
                </div>
                <div className="input-actions">
                  <button
                    onClick={validateText}
                    disabled={loading || !text.trim()}
                    className="btn btn-validate"
                  >
                    {loading ? (
                      <>
                        <div className="spinner"></div>
                        Validating Citations...
                      </>
                    ) : (
                      "Validate Citations"
                    )}
                  </button>
                  <button onClick={clearAll} className="btn btn-clear">
                    Clear
                  </button>
                </div>
              </div>
            )}

            {uploadMethod === "json" && (
              <div className="json-upload-area dev-only">
                <div className="json-input-container">
                  <textarea
                    value={jsonInput}
                    onChange={(e) => setJsonInput(e.target.value)}
                    placeholder='[{"citation":"410 U.S. 113","normalized_citations":["410 U.S. 113"],"start_index":0,"end_index":11,"status":200,"clusters":[]}]'
                    className="json-input-legal"
                  />
                </div>
                <div className="input-actions">
                  <button
                    onClick={validateJSON}
                    disabled={loading || !jsonInput.trim()}
                    className="btn btn-validate"
                  >
                    {loading ? (
                      <>
                        <div className="spinner"></div>
                        Processing...
                      </>
                    ) : (
                      "Process Citation Data"
                    )}
                  </button>
                  <button onClick={clearAll} className="btn btn-clear">
                    Clear
                  </button>
                </div>
              </div>
            )}

            {error && (
              <div className="error-message-legal">
                <div className="error-icon">⚠️</div>
                <span>{error}</span>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="results-section-legal">
            <div className="results-header-legal">
              <h2>Validation Results</h2>
              {results && (
                <button onClick={exportResults} className="btn btn-export">
                  📥 Export Report
                </button>
              )}
            </div>

            <div className="results-content-legal">
              {!results ? (
                <div className="results-empty-legal">
                  <div className="empty-icon">📋</div>
                  <h3>Ready to validate citations</h3>
                  <p>Upload a PDF brief or paste text to get started</p>
                </div>
              ) : (
                <div className="results-data-legal">
                  {getValidationSummary()}
                  
                  {/* Citation Results */}
                  <div className="citations-results">
                    <h3>Citation Details</h3>
                    <div className="citations-list-legal">
                      {results.citations.map((citation, index) => (
                        <div key={index} className={`citation-card-legal ${citation.verified ? 'valid' : 'invalid'}`}>
                          <div className="citation-header-legal">
                            <div className="citation-text-legal">
                              <code className="citation-code-legal">{citation.raw}</code>
                              {citation.normalized !== citation.raw && (
                                <div className="citation-normalized-legal dev-only">
                                  Normalized: <code>{citation.normalized}</code>
                                </div>
                              )}
                            </div>
                            <div className={`citation-status-legal ${citation.verified ? 'verified' : 'invalid'}`}>
                              {citation.verified ? (
                                <>
                                  <span className="status-icon">✅</span>
                                  <span>Verified</span>
                                </>
                              ) : (
                                <>
                                  <span className="status-icon">⚠️</span>
                                  <span>Needs Review</span>
                                </>
                              )}
                            </div>
                          </div>
                          
                          <div className="citation-details-legal">
                            <div className="citation-meta-legal">
                              <span className="meta-item-legal">
                                <strong>Reporter:</strong> {citation.reporter || "Unknown"}
                              </span>
                              <span className="meta-item-legal dev-only">
                                <strong>Position:</strong> Characters {citation.start_char}-{citation.end_char}
                              </span>
                            </div>
                            
                            {citation.note && (
                              <div className="citation-note-legal">
                                <div className="note-icon">💡</div>
                                <div className="note-text">
                                  <strong>Issue:</strong> {citation.note}
                                </div>
                              </div>
                            )}
                            
                            {citation.source_url && (
                              <div className="citation-source-legal">
                                <a 
                                  href={citation.source_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="source-link-legal"
                                >
                                  📖 View Full Case on CourtListener
                                </a>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
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