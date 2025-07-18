from django.shortcuts import render
import math
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from .utils import *

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


class addCPU(APIView):

    def post(self, request):
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})
        
        cpuData = {
            'model': getModel(data.get('name')),
            'brand': specs.get('Manufacturer'),
            'series': getSeries(specs.get('Series')),
            'generation': getGeneration(data.get('name')), #####################test with x3d
            'socket': specs.get('Socket'),
            'architecture': specs.get('Microarchitecture'),
            'coreCount': specs.get('Core Count'),
            'threadCount': specs.get('Thread Count'),
            'boostClock': getSpeed(specs.get('Performance Core Boost Clock')),
            'TDP': getWattage(specs.get('TDP')),
            'cacheSize': getCacheSize(specs.get('L2 Cache'), specs.get('L3 Cache')),
            'coolerIncluded': specs.get('Includes Cooler'),
            'integratedGPU': specs.get('Integrated Graphics'), ############### check if None works fine
            'price': math.ceil(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        serializer = CPUSerializer(data=cpuData)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        