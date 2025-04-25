import { useState, useEffect } from "react";
import Loader from "./Loader";

const AVAILABLE_MODELS = [
  "llama3",
  "llama3.1",
  "llama3.2",
  "mistral",
  "nous-hermes2",
  "codellama",
  "codellama:13b-instruct",
];

export default function ComparePolicyPanel({ onResponse }) {
  const [file, setFile] = useState(null);
  const [selectedStandard, setSelectedStandard] = useState("");
  const [selectedModel, setSelectedModel] = useState(AVAILABLE_MODELS[0]);
  const [loading, setLoading] = useState(false);
  const [standards, setStandards] = useState([]);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");
  const [loaderMessage, setLoaderMessage] = useState("");

  useEffect(() => {
    const fetchEmbeddedStandards = async () => {
      const res = await fetch("http://localhost:5001/api/embedded-standards");
      const result = await res.json();
      setStandards(result.standards || []);
    };
    fetchEmbeddedStandards();
  }, []);

  const handleFileChange = (e) => {
    if (loading) return;
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading || !file || !selectedStandard || !selectedModel) return;

    setLoading(true);
    setLoaderMessage(
      `Analyzing policy against ${selectedStandard} using ${selectedModel}...`
    );
    setError("");
    onResponse(""); // Clear previous response

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("standard", selectedStandard);
      formData.append("llm", selectedModel);

      const res = await fetch("http://localhost:5001/api/compare", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();

      if (res.ok && result.result) {
        onResponse(result.result);
      } else {
        setError(result.error || "An error occurred during comparison.");
        onResponse(result.error || "An error occurred during comparison.");
      }
    } catch (err) {
      console.error("Error submitting policy comparison:", err);
      setError("Failed to connect to backend.");
      onResponse("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Full-screen Loader */}
      <Loader
  isOpen={loading}
  message={loaderMessage}
  onCancel={() => {
    setLoading(false);
    setError(" Comparison cancelled by user.");
    onResponse("Comparison was cancelled by the user.");
  }}
/>

      {error && (
        <div className="bg-red-900/30 border border-red-700 text-red-300 p-2 rounded text-xs mb-2">
          {error}
        </div>
      )}

      <div className={`mb-4 ${loading ? "opacity-70" : ""}`}>
        <label className="block text-sm font-medium mb-2">
          Upload Company Policy
        </label>
        <div
          className={`relative border border-gray-700 rounded bg-gray-800 p-4 ${
            loading ? "pointer-events-none" : ""
          }`}
        >
          <input
            type="file"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            disabled={loading}
          />
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-300">
              {fileName || "Select a file..."}
            </span>
            <button
              className={`bg-gray-700 hover:bg-gray-600 text-white text-xs py-1 px-3 rounded ${
                loading ? "opacity-50 cursor-not-allowed" : ""
              }`}
              disabled={loading}
            >
              Browse
            </button>
          </div>
        </div>
        <p className="text-xs text-gray-400 mt-1">
          Accepted formats: PDF, DOCX, DOC, TXT
        </p>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Select Regulation to Compare
        </label>
        <select
          className={`w-full p-2 bg-gray-800 text-white rounded border border-gray-700 ${
            loading ? "opacity-70 cursor-not-allowed" : ""
          }`}
          value={selectedStandard}
          onChange={(e) => !loading && setSelectedStandard(e.target.value)}
          disabled={loading}
        >
          <option value="">-- Choose a standard --</option>
          {standards.map((standard) => (
            <option key={standard} value={standard}>
              {standard}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Select LLM Model
        </label>
        <select
          className={`w-full p-2 bg-gray-800 text-white rounded border border-gray-700 ${
            loading ? "opacity-70 cursor-not-allowed" : ""
          }`}
          value={selectedModel}
          onChange={(e) => !loading && setSelectedModel(e.target.value)}
          disabled={loading}
        >
          {AVAILABLE_MODELS.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading || !file || !selectedStandard || !selectedModel}
        className={`w-full py-2 px-4 rounded transition-colors ${
          loading || !file || !selectedStandard || !selectedModel
            ? "bg-gray-600 cursor-not-allowed"
            : "bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600"
        } text-white font-medium`}
      >
        Compare Policy
      </button>
    </div>
  );
}
