import { useState } from "react";
import { submitQuery, uploadStandard } from "../api";
import Loader from "./Loader";

export default function QueryPanel({ onResponse }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [standardName, setStandardName] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [error, setError] = useState("");
  const [uploadError, setUploadError] = useState("");
  const [loaderMessage, setLoaderMessage] = useState("");

  // Combined loading state for disabling UI elements
  const isLoading = loading || uploadLoading;

  const handleFileChange = (e) => {
    if (isLoading) return;
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (isLoading || !file || !standardName) return;

    setUploadLoading(true);
    setLoaderMessage(`Uploading and processing ${standardName}...`);
    setUploadSuccess(false);
    setUploadError("");

    try {
      const result = await uploadStandard(file, standardName);
      if (result.added) {
        setUploadSuccess(true);
        setStandardName("");
        setFile(null);
      } else {
        setUploadError(result.error || "Upload failed");
      }
    } catch (error) {
      console.error("Error uploading standard:", error);
      setUploadError("Failed to upload standard");
    } finally {
      setUploadLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading || !query.trim()) return;

    setLoading(true);
    setLoaderMessage("Processing your compliance query...");
    setError("");

    try {
      const result = await submitQuery(query);
      if (result) {
        onResponse(result.formattedAnswer || result.answer);
      }
    } catch (error) {
      console.error("Error submitting query:", error);
      setError("Failed to process query");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Query Section */}
      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
        <h3 className="text-sm font-medium mb-3">Ask About Compliance</h3>

        {error && (
          <div className="bg-red-900/30 border border-red-700 text-red-300 p-2 rounded text-xs mb-3">
            {error}
          </div>
        )}

        <div className="space-y-3">
          <div>
            <label className="block text-xs text-gray-400 mb-1">
              Your Query
            </label>
            <textarea
              className={`w-full p-2 bg-gray-700 text-white rounded h-24 ${
                isLoading ? "opacity-70 cursor-not-allowed" : ""
              }`}
              placeholder="e.g., What are the data breach reporting requirements?"
              value={query}
              onChange={(e) => !isLoading && setQuery(e.target.value)}
              disabled={isLoading}
            ></textarea>
          </div>

          <button
            onClick={handleSubmit}
            disabled={isLoading || !query.trim()}
            className={`w-full py-2 px-4 rounded transition-colors ${
              isLoading || !query.trim()
                ? "bg-gray-600 cursor-not-allowed opacity-70"
                : "bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600"
            } text-white font-medium`}
          >
            Submit Query
          </button>
        </div>
      </div>
      {/* Full-screen Loader */}
      <Loader
  isOpen={loading}
  message={loaderMessage}
  onCancel={() => {
    setLoading(false);
    setError("⛔️  cancelled by user.");
    onResponse("  cancelled by the user.");
  }}
/>

      {/* Upload Standard Section */}
      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
        <h3 className="text-sm font-medium mb-3">
          Upload New Compliance Standard
        </h3>

        {uploadSuccess && (
          <div className="bg-green-900/30 border border-green-700 text-green-300 p-2 rounded text-xs mb-3">
            Standard uploaded successfully!
          </div>
        )}

        {uploadError && (
          <div className="bg-red-900/30 border border-red-700 text-red-300 p-2 rounded text-xs mb-3">
            {uploadError}
          </div>
        )}

        <div className="space-y-3">
          <div>
            <label className="block text-xs text-gray-400 mb-1">
              Standard Name
            </label>
            <input
              type="text"
              className={`w-full p-2 bg-gray-700 text-white rounded ${
                isLoading ? "opacity-70 cursor-not-allowed" : ""
              }`}
              placeholder="e.g., GDPR, HIPAA, NIST"
              value={standardName}
              onChange={(e) => !isLoading && setStandardName(e.target.value)}
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-xs text-gray-400 mb-1">
              Upload PDF Document
            </label>
            <div
              className={`relative border border-gray-700 rounded bg-gray-700 p-2 ${
                isLoading ? "pointer-events-none" : ""
              }`}
            >
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={isLoading}
              />
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-300">
                  {file ? file.name : "Select a file..."}
                </span>
                <button
                  className={`bg-gray-600 hover:bg-gray-500 text-white text-xs py-1 px-2 rounded ${
                    isLoading ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                  disabled={isLoading}
                >
                  Browse
                </button>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Accepted formats: PDF, DOC, DOCX, TXT
            </p>
          </div>

          <button
            onClick={handleUpload}
            disabled={isLoading || !file || !standardName}
            className={`w-full py-1.5 px-4 rounded transition-colors ${
              isLoading || !file || !standardName
                ? "bg-gray-600 cursor-not-allowed opacity-70"
                : "bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600"
            } text-white text-sm font-medium`}
          >
            Upload Standard
          </button>
        </div>
      </div>

      
    </div>
  );
}
