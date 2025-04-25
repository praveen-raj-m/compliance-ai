// import { useState } from "react";
// import UploadForm from "./components/Uploadform";
// import StandardDropdown from "./components/StandardDropdown";
// import QueryBox from "./components/QueryBox";
// import ResultsPanel from "./components/ResultsPanel";
// import Loader from "./components/Loader";
// import BlurText from "./components/BlurText";
// import Aurora from "./components/Aurora";

// const handleAnimationComplete = () => {
//   console.log("Animation completed!");
// };

// function App() {
//   const [selectedStandard, setSelectedStandard] = useState(null);
//   const [response, setResponse] = useState("");
//   const [loading, setLoading] = useState(false);

//   return (
//     <div className=" bg-gray-950 w-screen h-screen text-white flex flex-col">
//       <Aurora
//         colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
//         blend={1.0}
//         amplitude={1.0}
//         speed={0.7}
//       />

//       <main className="flex flex-1">
//         {/* Sidebar */}
//         <div className="w-full max-w-sm p-10 border-r border-gray-800 space-y-10">
//           <UploadForm onUpload={(msg) => alert(msg)} />
//           <StandardDropdown onSelect={setSelectedStandard} />
//           <QueryBox onResult={setResponse} setLoading={setLoading} />
//         </div>

//         {/* Main Panel */}
//         <div className="flex-1 p-6 overflow-y-auto">
//           {loading ? <Loader /> : <ResultsPanel result={response} />}
//         </div>
//       </main>
//     </div>
//   );
// }
// export default App;

import SidebarTabs from "./components/SidebarTabs";
import ResponseBox from "./components/ResponseBox";
import { useState } from "react";
import Aurora from "./components/Aurora";
import TrueFocus from "./components/TrueFocus";

function App() {
  const [responseText, setResponseText] = useState("");

  return (
    <div className="flex flex-col w-screen min-h-screen bg-gray-900 text-white">
      <Aurora
        colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
        blend={0.5}
        amplitude={1.0}
        speed={0.7}
      />

      <header className="relative z-9 px-6 border-b border-gray-800">
        <div className="flex flex-col items-center justify-between">
          <div className="flex flex-col items-center space-x-2">
            <div className="flex pb-2">
            <TrueFocus
              sentence="Ask Analyze Align"
              manualMode={false}
              blurAmount={1.5}
              borderColor="skyblue"
              animationDuration={1}
              pauseBetweenAnimations={0.7}
            />
            </div>
            <h2>AI-powered compliance, built for clarity and control </h2>
          </div>
  
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden relative z-10">
        <aside className="w-[400px] border-r border-gray-800 flex flex-col">
          <div className="flex p-6 overflow-y-auto">
            <SidebarTabs onResponse={setResponseText} />
          </div>
          <div className="p-2 border-t border-gray-800 text-xs text-gray-500">
            All processing happens locally, ensuring data privacy
          </div>
        </aside>

        <main className="flex-1 p-6 overflow-y-auto">
          <ResponseBox text={responseText} />
        </main>
      </div>
    </div>
  );
}

export default App;
