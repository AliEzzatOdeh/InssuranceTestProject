from rest_framework import generics
from .serializers import RiskSerializer
from .models import Risk

class GetAllRiskTypes(generics.ListCreateAPIView):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

class GetRiskType(generics.ListCreateAPIView):
    serializer_class = RiskSerializer

    def get_queryset(self):

        riskname = self.kwargs['riskname']
        return Risk.objects.filter(name=riskname) 

    
