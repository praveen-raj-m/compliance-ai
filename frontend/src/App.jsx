import { useState } from "react";
import UploadForm from "./components/Uploadform";
import StandardDropdown from "./components/StandardDropdown";
import QueryBox from "./components/QueryBox";
import ResultsPanel from "./components/ResultsPanel";
import Loader from "./components/Loader";
import BlurText from "./components/BlurText";
import Aurora from "./components/Aurora";



const handleAnimationComplete = () => {
  console.log("Animation completed!");
};

function App() {
  const [selectedStandard, setSelectedStandard] = useState(null);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div className=" bg-gray-950 w-screen h-screen text-white flex flex-col">
      <Aurora
        colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
        blend={1.0}
        amplitude={1.0}
        speed={0.7}
      />


      <main className="flex flex-1">
        {/* Sidebar */}
        <div className="w-full max-w-sm p-6 border-r border-gray-800 space-y-6">
          <UploadForm onUpload={(msg) => alert(msg)} />
          <StandardDropdown onSelect={setSelectedStandard} />
          <QueryBox onResult={setResponse} setLoading={setLoading} />
        </div>

        {/* Main Panel */}
        <div className="flex-1 p-6 overflow-y-auto">
          {loading ? <Loader /> : <ResultsPanel result={response} />}
        </div>
      </main>
    </div>
  );
}
export default App;
