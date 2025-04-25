import { useState } from "react";
import QueryPanel from "./QueryPanel";
import ComparePolicyPanel from "./ComparePolicyPanel";

export default function SidebarTabs({ onResponse }) {
  const [activeTab, setActiveTab] = useState("query");

  const tabBase =
    "px-6 py-3 text-sm font-medium transition-all duration-200 border-b-2 focus:outline-none";
  const activeStyles =
    "!bg-transparent !text-white border-white hover:border-white";
  const inactiveStyles =
    "!bg-transparent !text-gray-400 border-transparent hover:!text-white hover:border-gray-500";

  return (
    <div className="w-full max-w-sm space-y-6">
      <div className="flex mb-4">
        <button
          className={`${tabBase} ${
            activeTab === "query" ? activeStyles : inactiveStyles
          }`}
          onClick={() => setActiveTab("query")}
        >
          Query Regulations
        </button>
        <button
          className={`${tabBase} ${
            activeTab === "compare" ? activeStyles : inactiveStyles
          }`}
          onClick={() => setActiveTab("compare")}
        >
          Check Company Policy
        </button>
      </div>

      {activeTab === "query" ? (
        <QueryPanel onResponse={onResponse} />
      ) : (
        <ComparePolicyPanel onResponse={onResponse} />
      )}
    </div>
  );
}
