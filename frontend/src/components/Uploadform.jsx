import { useState } from "react";

const UploadForm = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [type, setType] = useState("compliance");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Select a file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);

    const res = await fetch("http://localhost:5000/api/upload", {
      method: "POST",
      body: formData,
    });

    const result = await res.json();
    onUpload(result.message);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-gray-900 text-gray-100 p-5 rounded border border-gray-700">
      <label className="block text-sm font-medium">Upload PDF</label>
      <select
        className="w-full p-2 bg-gray-800 border border-gray-700 rounded text-sm"
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        <option value="compliance">Compliance Document</option>
        <option value="company">Company Policy</option>
      </select>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="w-full text-sm bg-gray-800 text-gray-200 p-2 border border-gray-700 rounded"
      />
      <button className="w-full bg-blue-600 hover:bg-blue-700 text-white p-2 rounded text-sm">
        Upload
      </button>
    </form>
  );
};

export default UploadForm;
