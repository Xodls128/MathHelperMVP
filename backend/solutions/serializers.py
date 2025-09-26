from rest_framework import serializers
from .models import SolutionAnalysis

class SolutionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionAnalysis
        fields = "__all__"   
# MVP니까 모든 필드 노출 
#(problem_image, answer_image, student_image, 
# gpt_response, created_at)
