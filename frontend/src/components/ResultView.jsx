export default function ResultView({ result }) {
  if (!result) return null;

  return (
    <div className="result-view">
      <h2>분석 결과</h2>

      {/* 오버레이 이미지 */}
      {result.overlay_image && (
        <img
          src={result.overlay_image}
          alt="분석된 풀이"
          style={{ maxWidth: "100%", marginTop: "1rem" }}
        />
      )}
    </div>
  );
}
