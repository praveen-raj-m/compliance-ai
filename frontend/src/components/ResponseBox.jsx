import { useState, useEffect } from "react";
import Loader from "./Loader";

export default function ResponseBox({ text }) {
  const [loading, setLoading] = useState(false);
  const [parsedResponse, setParsedResponse] = useState({
    answer: "",
    sources: [],
  });
  const [showReferences, setShowReferences] = useState(false);
  const [localText, setLocalText] = useState(text);

  useEffect(() => {
    if (text) {
      setLoading(true);
      setLocalText(text);

      const parseResponse = () => {
        try {
          if (text.includes("Sources:")) {
            const parts = text.split("Sources:");
            return {
              answer: parts[0].trim(),
              sources: parts[1]?.trim().split("\n").filter(Boolean) || [],
            };
          }
          return { answer: text, sources: [] };
        } catch {
          return { answer: text, sources: [] };
        }
      };

      const timeout = setTimeout(() => {
        setParsedResponse(parseResponse());
        setLoading(false);
        setShowReferences(false);
      }, 300);

      return () => clearTimeout(timeout);
    } else {
      setParsedResponse({ answer: "", sources: [] });
      setShowReferences(false);
      setLocalText("");
    }
  }, [text]);

  const handleClear = () => {
    setParsedResponse({ answer: "", sources: [] });
    setShowReferences(false);
    setLocalText("");
  };

  return (
    <div className="mt-6 p-6 min-h-[200px] bg-gray-900 rounded-lg border border-gray-700 text-sm text-white whitespace-pre-wrap relative flex flex-col justify-between">
      <Loader isOpen={loading} message="Processing response..." />

      {!localText ? (
        <div className="flex items-center justify-center h-full text-gray-500 text-sm">
          Ask a query to get started.
        </div>
      ) : (
        <>
          <div className="mb-4">{parsedResponse.answer}</div>

          {parsedResponse.sources.length > 0 && (
            <div className="pt-2">
              <button
                onClick={() => setShowReferences(!showReferences)}
                className="text-xs text-gray-400 underline hover:text-white transition"
              >
                {showReferences ? "Hide References" : "Show References"}
              </button>

              {showReferences && (
                <ul className="mt-3 space-y-1 text-gray-400 border-t border-gray-700 pt-3">
                  {parsedResponse.sources.map((source, index) => (
                    <li key={index} className="pl-3 border-l border-gray-700">
                      {source}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

          <div className="mt-6 text-right">
            <button
              onClick={handleClear}
              className="text-xs text-gray-400 underline hover:text-white transition"
            >
              Clear Response
            </button>
          </div>
        </>
      )}
    </div>
  );
}
