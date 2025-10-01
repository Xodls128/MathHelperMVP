from django.db import models

class SolutionAnalysis(models.Model):
    problem_image = models.ImageField(upload_to="problems/")
    answer_image = models.ImageField(upload_to="answers/")
    student_image = models.ImageField(upload_to="students/")
    gpt_response = models.TextField()  # GPT 응답 원본 그대로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    overlay_image = models.ImageField(upload_to="overlays/", null=True, blank=True)

    def __str__(self):
        return f"Analysis {self.id} - {self.created_at}"
