import os
import uuid
from PIL import Image, ImageDraw, ImageFont

def draw_overlay(student_image_path, annotations, media_root="media"):
    """
    학생 풀이 이미지 위에 GPT 분석 결과를 오버레이한 이미지를 생성
    :param student_image_path: 원본 학생 풀이 이미지 경로 (analysis.student_image.path)
    :param annotations: GPT가 반환한 JSON (list of dict)
    :param media_root: MEDIA_ROOT 기본값
    :return: 저장된 합성 이미지의 절대 경로
    """
    img = Image.open(student_image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 폰트 설정 (운영체제에 따라 다름)
    try:
        font_expr = ImageFont.truetype("arial.ttf", 20)
        font_exp = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        # 서버에 arial.ttf가 없을 수 있음 → 기본 폰트 fallback
        font_expr = ImageFont.load_default()
        font_exp = ImageFont.load_default()

    for ann in annotations:
        x1, y1, x2, y2 = ann.get("x1"), ann.get("y1"), ann.get("x2"), ann.get("y2")
        correct_expr = ann.get("correct_expr", "")
        explanation = ann.get("logical_explanation", "")

        # 틀린 부분 박스 (빨간색)
        if None not in (x1, y1, x2, y2):
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # 올바른 식 (파란색)
        if correct_expr:
            draw.text((x1, y2 + 5), correct_expr, fill="blue", font=font_expr)

        # 간단 설명 (검정색)
        if explanation:
            draw.text((x1, y2 + 30), explanation, fill="black", font=font_exp)

    # 저장 경로 생성
    overlay_dir = os.path.join(media_root, "overlays")
    os.makedirs(overlay_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(overlay_dir, filename)

    img.save(output_path, format="JPEG")
    return output_path
