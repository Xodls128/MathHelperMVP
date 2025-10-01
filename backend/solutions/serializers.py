from rest_framework import serializers
from .models import SolutionAnalysis

class SolutionAnalysisSerializer(serializers.ModelSerializer):
    problem_image = serializers.ImageField(read_only=True)
    answer_image = serializers.ImageField(read_only=True)
    student_image = serializers.ImageField(read_only=True)
    overlay_image = serializers.ImageField(read_only=True)

    class Meta:
        model = SolutionAnalysis
        fields = "__all__"   
# MVP니까 모든 필드 노출 
#(problem_image, answer_image, student_image, 
# gpt_response, created_at)
