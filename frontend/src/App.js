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
      case "high": return "text-green-600 bg-green-50";
      case "medium": return "text-yellow-600 bg-yellow-50";
      case "low": return "text-red-600 bg-red-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  const getStatusColor = (verified) => {
    return verified 
      ? "text-green-600 bg-green-50 border-green-200" 
      : "text-red-600 bg-red-50 border-red-200";
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Strike Cite</h1>
              <p className="text-gray-600 mt-1">U.S. Legal Citation Validator</p>
            </div>
            <div className="text-sm text-gray-500">
              {reporters.length} reporters loaded
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Mode Selection */}
        <div className="mb-6">
          <div className="flex space-x-4">
            <button
              onClick={() => setMode("text")}
              className={`px-4 py-2 rounded-lg font-medium ${
                mode === "text" 
                  ? "bg-blue-600 text-white" 
                  : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
              }`}
            >
              Full Pipeline (Text Input)
            </button>
            <button
              onClick={() => setMode("json")}
              className={`px-4 py-2 rounded-lg font-medium ${
                mode === "json" 
                  ? "bg-blue-600 text-white" 
                  : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
              }`}
            >
              Validation Service (LOOKUP_JSON)
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {mode === "text" ? "Legal Text Input" : "LOOKUP_JSON Input"}
            </h2>
            
            {mode === "text" ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter legal text containing citations:
                </label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Enter legal text with citations, e.g., 'The landmark case of Roe v. Wade, 410 U.S. 113 (1973), established...'"
                  className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-sm text-gray-500 mt-2">
                  This will call CourtListener API to find citations, then validate them.
                </p>
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter LOOKUP_JSON from CourtListener API:
                </label>
                <textarea
                  value={jsonInput}
                  onChange={(e) => setJsonInput(e.target.value)}
                  placeholder='[{"citation": "410 US 113", "normalized_citations": ["410 U.S. 113"], "start_index": 22, "end_index": 32, "status": 200, "clusters": [{"url": "https://..."}]}]'
                  className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                />
                <p className="text-sm text-gray-500 mt-2">
                  This validates pre-processed citations from CourtListener.
                </p>
              </div>
            )}

            <div className="flex space-x-3 mt-4">
              <button
                onClick={mode === "text" ? validateText : validateJSON}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
                className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
              >
                Clear
              </button>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Validation Results</h2>
              {results && (
                <button
                  onClick={exportResults}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Export JSON
                </button>
              )}
            </div>

            {!results ? (
              <div className="text-center py-12 text-gray-500">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="mt-2">No validation results yet</p>
                <p className="text-sm">Enter text or JSON above to validate citations</p>
              </div>
            ) : (
              <div>
                {/* Summary */}
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-gray-900">{results.summary.total}</div>
                      <div className="text-sm text-gray-600">Total</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-600">{results.summary.verified}</div>
                      <div className="text-sm text-gray-600">Verified</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-red-600">{results.summary.unverified}</div>
                      <div className="text-sm text-gray-600">Unverified</div>
                    </div>
                    <div>
                      <div className={`text-2xl font-bold ${getConfidenceColor(results.summary.confidence).split(' ')[0]}`}>
                        {results.summary.confidence.toUpperCase()}
                      </div>
                      <div className="text-sm text-gray-600">Confidence</div>
                    </div>
                  </div>
                </div>

                {/* Citations List */}
                <div className="space-y-4">
                  {results.citations.map((citation, index) => (
                    <div key={index} className={`border rounded-lg p-4 ${getStatusColor(citation.verified)}`}>
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex-1">
                          <div className="font-mono text-sm font-semibold">
                            {citation.raw}
                          </div>
                          {citation.normalized !== citation.raw && (
                            <div className="text-sm text-gray-600 mt-1">
                              Normalized: {citation.normalized}
                            </div>
                          )}
                        </div>
                        <div className={`px-2 py-1 rounded text-xs font-medium ${
                          citation.verified 
                            ? "bg-green-100 text-green-800" 
                            : "bg-red-100 text-red-800"
                        }`}>
                          {citation.verified ? "VERIFIED" : "UNVERIFIED"}
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium">Reporter:</span> {citation.reporter || "Unknown"}
                        </div>
                        <div>
                          <span className="font-medium">Position:</span> {citation.start_char}-{citation.end_char}
                        </div>
                      </div>
                      
                      {citation.note && (
                        <div className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
                          <span className="font-medium">Note:</span> {citation.note}
                        </div>
                      )}
                      
                      {citation.source_url && (
                        <div className="mt-2">
                          <a 
                            href={citation.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm underline"
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

        {/* Footer Info */}
        <div className="mt-12 text-center">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">About Strike Cite</h3>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Layer A: Validation Microservice</h4>
                <p className="text-sm text-gray-600">
                  Reusable core that processes LOOKUP_JSON from CourtListener API and validates citations 
                  against our comprehensive legal reporter database.
                </p>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Layer B: Full Pipeline</h4>
                <p className="text-sm text-gray-600">
                  Complete text-to-validation workflow that calls CourtListener API for citation extraction,
                  then validates using Layer A microservice.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
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