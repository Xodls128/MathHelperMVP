from django.urls import path
from .views import SolutionAnalysisView

urlpatterns = [
    path("analyze/", SolutionAnalysisView.as_view(), name="solution-analyze"),
]
