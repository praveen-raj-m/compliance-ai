import { useState } from "react";

const QueryBox = ({ onResult, setLoading }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    const res = await fetch("http://localhost:5000/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: query }),
    });

    const result = await res.json();
    onResult(result.answer);
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-gray-900 text-gray-100 p-5 rounded border border-gray-700">
      <label className="text-sm font-medium">Ask a Question</label>
      <textarea
        rows={3}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full bg-gray-800 text-gray-200 p-2 border border-gray-700 rounded text-sm"
        placeholder="e.g. What are the breach notification rules?"
      />
      <button className="w-full bg-green-600 hover:bg-green-700 text-white p-2 rounded text-sm">
        Submit
      </button>
    </form>
  );
};

export default QueryBox;
