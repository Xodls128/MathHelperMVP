import { useState } from "react";
import UploadForm from "../components/UploadForm";
import ResultView from "../components/ResultView";

export default function AnalysisPage() {
  const [result, setResult] = useState(null);

  return (
    <div>
      <h1>문제 풀이 검토</h1>
      <UploadForm onResult={setResult} />
      <ResultView result={result} />
    </div>
  );
}
