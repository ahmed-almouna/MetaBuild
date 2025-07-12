from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET'])
def getBuild(request, format=None):

    dummy_parts = [
        {
            "type": "CPU",
            "name": "Intel Core i5-12400F",
            "price": 160,
            "socket": "LGA1700"
        },
        {
            "type": "GPU",
            "name": "NVIDIA RTX 4060",
            "price": 300,
            "vram": "8 GB"
        },
        {
            "type": "RAM",
            "name": "Corsair Vengeance 16GB DDR5",
            "price": 80,
            "speed": "6000 MHz"
        }
    ]
    return Response(dummy_parts)


class addCPU(CreateAPIView):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer