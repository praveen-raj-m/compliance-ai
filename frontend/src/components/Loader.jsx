// import React from "react";

// const Loader = ({
//   isOpen = false,
//   message = "Processing...",
//   overlay = true,
// }) => {
//   if (!isOpen) return null;

//   return (
//     <div
//       className={`fixed inset-0 z-50 flex items-center justify-center ${
//         overlay ? "bg-black/50 backdrop-blur-sm" : ""
//       }`}
//     >
//       <div className="bg-gray-900 border border-gray-700 rounded-lg p-8 shadow-xl">
//         <div className="flex flex-col items-center">
//           <div className="w-16 h-16 border-4 border-t-red-500 border-r-pink-300 border-b-red-400 border-l-pink-400 border-solid rounded-full animate-spin mb-4"></div>
//           <p className="text-white text-center">{message}</p>
//         </div>
//       </div>
//     </div>
//   );
// };

// // Export a smaller inline version too for cases where a full overlay is too much
// export const InlineLoader = ({ size = "md", className = "" }) => {
//   const sizeClasses = {
//     sm: "w-4 h-4 border-2",
//     md: "w-8 h-8 border-3",
//     lg: "w-12 h-12 border-4",
//   };

//   const sizeClass = sizeClasses[size] || sizeClasses.md;

//   return (
//     <div className={`flex justify-center items-center ${className}`}>
//       <div
//         className={`${sizeClass} border-t-red-500 border-r-pink-300 border-b-red-400 border-l-pink-400 border-solid rounded-full animate-spin`}
//       ></div>
//     </div>
//   );
// };

// export default Loader;


// import React, { useEffect, useState } from "react";

// const tips = [
//   "Ensure your policies align with ISO 27001's control objectives.",
//   "Automate risk assessments to reduce manual errors.",
//   "Use version control for all compliance documents.",
//   "Maintain an auditable trail for every access request.",
//   "Test your incident response plan quarterly.",
//   "Align privacy practices with GDPR Article 5 principles.",
//   "Use NLP to monitor regulatory changes in real time.",
//   "Back up compliance logs in geographically separate locations.",
//   "Review vendor risk assessments annually.",
//   "Leverage AI for continuous control monitoring.",
//   "Classify data before applying protection policies.",
//   "Map regulatory requirements to internal controls regularly.",
//   "Use role-based access controls to enforce least privilege.",
//   "Document compliance exceptions and remediation steps.",
//   "Validate AI systems against bias and explainability standards."
// ];

// const Loader = (
//   isOpen = false,
//   message = "Processing...",
//   overlay = true,
// ) => {
//   if (!isOpen) return null;
//   const [tipIndex, setTipIndex] = useState(0);

//   useEffect(() => {
//     const interval = setInterval(() => {
//       setTipIndex((prev) => (prev + 1) % tips.length);
//     }, 4000); // Change tip every 4 seconds
//     return () => clearInterval(interval);
//   }, []);

//   return (
//     <div className="h-full w-full flex flex-col justify-center items-center bg-gray-900 text-white p-8 rounded-lg border border-gray-700">
//       <div className="mb-6 animate-spin border-t-4 border-pink-400 border-solid rounded-full w-16 h-16"></div>
//       <p className="text-sm text-gray-400 mb-2">Processing your request...</p>
//       <div className="text-center text-sm mt-4 px-6 py-3 border border-gray-600 rounded-md bg-gray-800 text-gray-300 transition-opacity duration-500 ease-in-out">
//         <span className="italic">💡 {tips[tipIndex]}</span>
//       </div>
//     </div>
//   );
// };

// export default Loader;


import React, { useEffect, useState } from "react";

const quotes = [
  "“Compliance is not a checkbox—it’s a commitment.”",
  "“Privacy is not an option—it’s a fundamental right.”",
  "“Strong controls prevent weak excuses.”",
  "“Audit trails tell the story of your integrity.”",
  "“Transparency builds trust—regulations demand it.”",
  "“Security is compliance’s strongest ally.”",
  "“Policy without enforcement is just a suggestion.”",
  "“Real-time monitoring beats reactive mitigation.”",
  "“Automate the boring, audit the critical.”",
  "“Good governance is good business.”",
  "“Compliance doesn’t slow you down—it keeps you standing.”",
  "“AI + GRC = smarter risk management.”",
  "“Document it, or it didn’t happen.”",
  "“Data ethics is the next frontier of compliance.”",
  "“Proactive compliance is cheaper than reactive penalties.”",
];

const Loader = ({ isOpen = false, message = "Processing...", overlay = true, onCancel }) => {
  const [quoteIndex, setQuoteIndex] = useState(0);

  useEffect(() => {
    if (!isOpen) return;

    const interval = setInterval(() => {
      setQuoteIndex((prev) => (prev + 1) % quotes.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center ${
        overlay ? "bg-black/50 backdrop-blur-sm" : ""
      }`}
    >
      <div className="bg-gray-900 border border-gray-700 rounded-lg p-8 shadow-xl w-full max-w-md text-center">
        <div className="flex flex-col items-center space-y-5">
          <div className="w-16 h-16 border-4 border-t-red-500 border-r-pink-300 border-b-red-400 border-l-pink-400 border-solid rounded-full animate-spin" />
          <p className="text-white text-base">{message}</p>
          <p className="text-sm text-gray-400 italic min-h-[60px] transition-opacity duration-500 ease-in-out">
            {quotes[quoteIndex]}
          </p>

          {onCancel && (
            <button
              onClick={onCancel}
              className="mt-2 px-4 py-1 text-sm rounded-md text-white bg-red-600 hover:bg-red-700 transition"
            >
              Stop
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// Optional mini inline spinner
export const InlineLoader = ({ size = "md", className = "" }) => {
  const sizeClasses = {
    sm: "w-4 h-4 border-2",
    md: "w-8 h-8 border-3",
    lg: "w-12 h-12 border-4",
  };

  const sizeClass = sizeClasses[size] || sizeClasses.md;

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div
        className={`${sizeClass} border-t-red-500 border-r-pink-300 border-b-red-400 border-l-pink-400 border-solid rounded-full animate-spin`}
      />
    </div>
  );
};

export default Loader;
