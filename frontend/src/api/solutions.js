import axios from "axios";

const API_BASE = "http://localhost:8000/api/solutions";

export async function analyzeSolution(problemImg, answerImg, studentImg) {
  const formData = new FormData();
  formData.append("problem_image", problemImg);
  formData.append("answer_image", answerImg);
  formData.append("student_image", studentImg);

  const response = await axios.post(`${API_BASE}/analyze/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data; // gpt_response 포함된 JSON
}
