import base64
import requests
import os
import json
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def call_gpt_api(problem_img, answer_img, student_img):
    """
    GPT API 호출 (이미지 3개 + 프롬프트 전달)
    반환: 딕셔너리 안에 리스트, (x1,y1,x2,y2,correct_expr,explanation)
    """
    # FileField/ImageField 경로를 base64로 변환
    def encode_image(image_field):
        with open(image_field.path, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

    try:
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
                        {"type": "text",
                            "text": """세 이미지를 비교하여 학생 풀이에서 틀린 부분을 찾아 JSON 배열로만 반환하세요.
형식:
[
  {"x1": <int>, "y1": <int>, "x2": <int>, "y2": <int>,
   "correct_expr": "<string>",
   "logical_explanation": "<string>"}
]
줄글 없이 JSON만 출력하세요."""

                        },
                        {"type": "image_url", "image_url": {"url": problem_b64}},
                        {"type": "image_url", "image_url": {"url": answer_b64}},
                        {"type": "image_url", "image_url": {"url": student_b64}}
                    ],
                }
            ],
            "temperature": 0.2,  # 최대한 일관된 JSON 형식 유도
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # HTTP 2xx가 아니면 예외 발생
        result = response.json()
        
        # .get()을 사용하여 안전하게 값 추출
        content = result.get("choices", [{}])[0].get("message", {}).get("content")

        if not content:
            print("API 응답에 content가 없습니다.")
            return []

        # JSON 부분만 정규식으로 추출
        match = re.search(r"\[.*\]", content, re.S)  # [ ... ] 블록 전체 잡기
        if match:
            try:
                annotations = json.loads(match.group())
                return annotations
            except json.JSONDecodeError:
                print("JSON 파싱 실패 (배열 추출 성공했지만 불완전). 원문 반환.")
                return []
        else:
            print("응답에서 JSON 배열을 찾을 수 없습니다.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"API 응답 파싱 오류: {e}")
        return []
    except Exception as e:
        print(f"이미지 인코딩 또는 기타 오류: {e}")
        return []
