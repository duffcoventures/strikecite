import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StrikeCite = () => {
  const [text, setText] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mode, setMode] = useState("text"); // "text" or "json"
  const [jsonInput, setJsonInput] = useState("");
  const [reporters, setReporters] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  // Load available reporters on component mount
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
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
      };
      reader.readAsText(file);
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
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-black tracking-tight">Strike Cite</h1>
              <p className="text-gray-600 text-sm mt-1">U.S. Legal Citation Validator</p>
            </div>
            <div className="text-xs text-gray-500 text-right">
              <div>{reporters.length} comprehensive legal reporters</div>
              <div className="text-xs text-gray-400">Federal • Regional • State • Specialized</div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Mode Selection */}
        <div className="mb-8">
          <div className="flex border border-gray-200 rounded-lg overflow-hidden w-fit">
            <button
              onClick={() => setMode("text")}
              className={`px-6 py-3 text-sm font-medium border-r border-gray-200 ${
                mode === "text" 
                  ? "bg-black text-white" 
                  : "bg-white text-gray-700 hover:bg-gray-50"
              }`}
            >
              Full Pipeline
            </button>
            <button
              onClick={() => setMode("json")}
              className={`px-6 py-3 text-sm font-medium ${
                mode === "json" 
                  ? "bg-black text-white" 
                  : "bg-white text-gray-700 hover:bg-gray-50"
              }`}
            >
              Validation Service
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            {mode === "text" 
              ? "Complete text processing with CourtListener API integration" 
              : "Direct validation of LOOKUP_JSON from CourtListener API"}
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="bg-white border border-gray-200 rounded-lg">
            <div className="border-b border-gray-200 px-6 py-4">
              <h2 className="text-lg font-semibold text-black">
                {mode === "text" ? "Legal Document Input" : "LOOKUP_JSON Input"}
              </h2>
            </div>
            
            <div className="p-6">
              {mode === "text" ? (
                <div>
                  <div 
                    className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
                      dragActive ? "border-black bg-gray-50" : "border-gray-300"
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    <textarea
                      value={text}
                      onChange={(e) => setText(e.target.value)}
                      placeholder="Paste legal text with citations here, or drag and drop a text file..."
                      className="w-full h-64 resize-none border-0 focus:ring-0 focus:outline-none bg-transparent text-sm"
                    />
                    <div className="absolute bottom-3 right-3 text-xs text-gray-400">
                      {text.length}/64,000 characters
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    ✓ Drag & drop text files • ✓ Up to 50 pages • ✓ Automatic citation extraction
                  </p>
                </div>
              ) : (
                <div>
                  <textarea
                    value={jsonInput}
                    onChange={(e) => setJsonInput(e.target.value)}
                    placeholder='[{"citation": "410 U.S. 113", "normalized_citations": ["410 U.S. 113"], "start_index": 22, "end_index": 32, "status": 200, "clusters": [{"url": "https://..."}]}]'
                    className="w-full h-64 px-4 py-3 border border-gray-200 rounded-lg font-mono text-xs resize-none focus:ring-1 focus:ring-black focus:border-black"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    ✓ Direct LOOKUP_JSON processing • ✓ Microservice validation • ✓ Enhanced error detection
                  </p>
                </div>
              )}

              <div className="flex items-center gap-3 mt-6">
                <button
                  onClick={mode === "text" ? validateText : validateJSON}
                  disabled={loading}
                  className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center text-sm font-medium"
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Validating...
                    </>
                  ) : (
                    "Validate Citations"
                  )}
                </button>
                
                <button
                  onClick={clearResults}
                  className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 text-sm font-medium"
                >
                  Clear
                </button>
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800 text-sm">⚠ {error}</p>
                </div>
              )}
            </div>
          </div>

          {/* Results Section */}
          <div className="bg-white border border-gray-200 rounded-lg">
            <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center">
              <h2 className="text-lg font-semibold text-black">Validation Results</h2>
              {results && (
                <button
                  onClick={exportResults}
                  className="text-black hover:text-gray-600 text-sm font-medium underline"
                >
                  Export JSON
                </button>
              )}
            </div>

            <div className="p-6">
              {!results ? (
                <div className="text-center py-12 text-gray-500">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <p className="text-gray-600 font-medium">No validation results yet</p>
                  <p className="text-sm text-gray-500 mt-1">Enter text or JSON above to validate citations</p>
                </div>
              ) : (
                <div>
                  {/* Summary Stats */}
                  <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
                    <div className="grid grid-cols-4 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-black">{results.summary.total}</div>
                        <div className="text-xs text-gray-600">TOTAL</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-green-700">{results.summary.verified}</div>
                        <div className="text-xs text-gray-600">VERIFIED</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-red-700">{results.summary.unverified}</div>
                        <div className="text-xs text-gray-600">INVALID</div>
                      </div>
                      <div>
                        <div className={`text-2xl font-bold ${getConfidenceColor(results.summary.confidence)}`}>
                          {results.summary.confidence.toUpperCase()}
                        </div>
                        <div className="text-xs text-gray-600">CONFIDENCE</div>
                      </div>
                    </div>
                  </div>

                  {/* Citations List */}
                  <div className="space-y-3">
                    {results.citations.map((citation, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                        <div className="flex justify-between items-start mb-3">
                          <div className="flex-1">
                            <div className="font-mono text-sm font-semibold text-black mb-1">
                              {citation.raw}
                            </div>
                            {citation.normalized !== citation.raw && (
                              <div className="text-xs text-gray-600 font-mono">
                                Normalized: {citation.normalized}
                              </div>
                            )}
                          </div>
                          <div className={`px-2 py-1 rounded-md text-xs font-medium border ${getStatusBadge(citation.verified)}`}>
                            {citation.verified ? "VERIFIED" : "INVALID"}
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 text-xs mb-3">
                          <div>
                            <span className="text-gray-500">Reporter:</span> 
                            <span className="ml-1 font-medium">{citation.reporter || "Unknown"}</span>
                          </div>
                          <div>
                            <span className="text-gray-500">Position:</span> 
                            <span className="ml-1 font-medium">{citation.start_char}-{citation.end_char}</span>
                          </div>
                        </div>
                        
                        {citation.note && (
                          <div className="mb-3 text-xs text-red-700 bg-red-50 p-2 rounded border border-red-200">
                            <span className="font-medium">⚠ Issue:</span> {citation.note}
                          </div>
                        )}
                        
                        {citation.source_url && (
                          <div>
                            <a 
                              href={citation.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-black hover:text-gray-600 text-xs underline font-medium"
                            >
                              View on CourtListener →
                            </a>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200">
          <div className="grid md:grid-cols-2 gap-8 text-sm">
            <div>
              <h3 className="font-semibold text-black mb-2">Layer A: Validation Microservice</h3>
              <p className="text-gray-600 text-xs leading-relaxed">
                Reusable core that processes LOOKUP_JSON from CourtListener API. Validates citations 
                against comprehensive legal reporter database with enhanced error detection.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-black mb-2">Layer B: Complete Pipeline</h3>
              <p className="text-gray-600 text-xs leading-relaxed">
                End-to-end workflow integrating CourtListener's citation extraction with Strike Cite's 
                validation intelligence for professional legal citation analysis.
              </p>
            </div>
          </div>
          
          <div className="mt-6 pt-4 border-t border-gray-100 text-center">
            <p className="text-xs text-gray-500">
              Powered by {reporters.length} comprehensive legal reporters • 
              CourtListener API integration • Professional citation validation
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <StrikeCite />
    </div>
  );
}

export default App;