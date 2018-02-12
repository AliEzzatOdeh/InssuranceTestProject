from django.urls import path
from .views import GetAllRiskTypes, GetRiskType

urlpatterns = [
    path(r'getAllRiskTypes/', GetAllRiskTypes.as_view()),
    path(r'getRiskType/<riskname>', GetRiskType.as_view()),
]