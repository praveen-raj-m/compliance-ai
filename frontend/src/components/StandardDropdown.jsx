import { useEffect, useState } from "react";

const StandardDropdown = ({ onSelect }) => {
  const [standards, setStandards] = useState([]);

  useEffect(() => {
    const fetchStandards = async () => {
      const res = await fetch("http://localhost:5000/api/standards");
      const result = await res.json();
      setStandards(result.standards || []);
    };
    fetchStandards();
  }, []);

  return (
    <div className="space-y-2 text-gray-100">
      <label className="text-sm font-medium">Select Regulation</label>
      <select
        onChange={(e) => onSelect(e.target.value)}
        className="w-full p-2 bg-gray-800 border border-gray-700 text-sm rounded"
      >
        <option value="">-- Choose --</option>
        {standards.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
    </div>
  );
};

export default StandardDropdown;
