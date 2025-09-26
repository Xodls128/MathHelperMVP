import base64
import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def call_gpt_api(problem_img, answer_img, student_img):
    """
    GPT API 호출 (이미지 3개 + 프롬프트 전달)
    """
    # FileField/ImageField 경로를 base64로 변환
    def encode_image(image_field):
        with open(image_field.path, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

    problem_b64 = encode_image(problem_img)
    answer_b64 = encode_image(answer_img)
    student_b64 = encode_image(student_img)

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "다음 세 이미지를 바탕으로 학생 풀이를 구조적으로 분석해줘. 형식: 1) 올바른 단계, 2) 오류 단계, 3) 개선 제안"},
                    {"type": "image_url", "image_url": {"url": problem_b64}},
                    {"type": "image_url", "image_url": {"url": answer_b64}},
                    {"type": "image_url", "image_url": {"url": student_b64}}
                ],
            }
        ],
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result["choices"][0]["message"]["content"]
