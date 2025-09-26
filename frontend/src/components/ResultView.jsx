export default function ResultView({ result }) {
  if (!result) return null;

  return (
    <div className="result-view">
      <h2>분석 결과</h2>
      <pre>{result.gpt_response}</pre>
    </div>
  );
}
