import { useState } from "react";
import { analyzeSolution } from "../api/solutions";

export default function UploadForm({ onResult }) {
  const [problemImg, setProblemImg] = useState(null);
  const [answerImg, setAnswerImg] = useState(null);
  const [studentImg, setStudentImg] = useState(null);
  const [preview, setPreview] = useState({}); // 썸네일 저장
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      if (type === "problem") setProblemImg(file);
      if (type === "answer") setAnswerImg(file);
      if (type === "student") setStudentImg(file);
      setPreview((prev) => ({
        ...prev,
        [type]: URL.createObjectURL(file),
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!problemImg || !answerImg || !studentImg) {
      alert("세 개의 이미지를 모두 업로드해야 합니다.");
      return;
    }
    setLoading(true);
    try {
      const result = await analyzeSolution(problemImg, answerImg, studentImg);
      onResult(result);
    } catch (err) {
      console.error(err);
      alert("분석 중 오류 발생");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>문제 이미지</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleFileChange(e, "problem")}
        />
        {preview.problem && <img src={preview.problem} alt="문제 미리보기" width="150" />}
      </div>

      <div>
        <label>답지 이미지</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleFileChange(e, "answer")}
        />
        {preview.answer && <img src={preview.answer} alt="답지 미리보기" width="150" />}
      </div>

      <div>
        <label>학생 풀이 이미지</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleFileChange(e, "student")}
        />
        {preview.student && <img src={preview.student} alt="풀이 미리보기" width="150" />}
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "분석 중..." : "분석하기"}
      </button>
    </form>
  );
}
