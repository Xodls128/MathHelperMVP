from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SolutionAnalysis
from .serializers import SolutionAnalysisSerializer
from .services import call_gpt_api

class SolutionAnalysisView(APIView):
    def post(self, request, *args, **kwargs):
        problem_img = request.FILES.get("problem_image")
        answer_img = request.FILES.get("answer_image")
        student_img = request.FILES.get("student_image")

        if not (problem_img and answer_img and student_img):
            return Response({"error": "모든 이미지가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # DB 저장 (gpt_response는 일단 빈 값으로)
        analysis = SolutionAnalysis.objects.create(
            problem_image=problem_img,
            answer_image=answer_img,
            student_image=student_img,
            gpt_response=""
        )

        # GPT 호출
        gpt_response = call_gpt_api(analysis.problem_image, analysis.answer_image, analysis.student_image)

        if gpt_response is None:
            analysis.delete()  # GPT 호출 실패 시, 생성했던 객체 삭제
            return Response(
                {"error": "AI 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        analysis.gpt_response = gpt_response
        analysis.save()

        serializer = SolutionAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
