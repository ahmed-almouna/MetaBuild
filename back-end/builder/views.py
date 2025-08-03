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
            'pcPartPickerId': data.get('id'),
            'model': getModel(data.get('name')),
            'brand': specs.get('Manufacturer'),
            'series': getSeries(specs.get('Series')),
            'generation': getGeneration(data.get('name')),
            'socket': specs.get('Socket'),
            'architecture': specs.get('Microarchitecture'),
            'coreCount': specs.get('Core Count'),
            'threadCount': specs.get('Thread Count'),
            'boostClock': getSpeed(specs.get('Performance Core Boost Clock')),
            'TDP': getNumber(specs.get('TDP')),
            'cacheSize': getCacheSize(specs.get('L2 Cache'), specs.get('L3 Cache')),
            'coolerIncluded': specs.get('Includes Cooler'),
            'integratedGPU': specs.get('Integrated Graphics'),
        }

        cpuSerializer = CPUSerializer(data=cpuData)

        if cpuSerializer.is_valid() != True:
            return Response(cpuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cpuInstance = cpuSerializer.save()

        priceData = {
            'CPUId': cpuInstance.id,
            'country': 'US',
            'available': True,
            'price': getPrice(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        priceSerializer = CPUPriceSerializer(data=priceData)

        if priceSerializer.is_valid():
            priceSerializer.save()
        
        return Response(cpuSerializer.data, status=status.HTTP_201_CREATED)



class addGPU(APIView):
    def post(self, request):
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})
        
        gpuData = {
            'pcPartPickerId': data.get('id'),
            'model': getModel(data.get('name'), type="GPU"),
            'brand': getBrand(specs.get('Chipset')),
            'manufacturer': specs.get('Manufacturer'),
            'name': getName(data.get('name')),
            'series': getGeneration(data.get('name'), type="GPU"),
            'boostClock': getNumber(specs.get('Boost Clock')),
            'TDP': getNumber(specs.get('TDP')),
            'VRAM': getNumber(specs.get('Memory')),
        }

        # Check if GPU with same model exists//////////////
        # existing_gpu = GPU.objects.filter(model=gpuData['model']).first()
        # if existing_gpu:
        #     # Get the current price for this GPU
        #     current_price = GPUPrice.objects.filter(GPUId=existing_gpu).first()
        #     if current_price and current_price.price <= getPrice(listings.get('lowestPrice')):
        #         # If existing price is lower or equal, return existing GPU data
        #         return Response(GPUSerializer(existing_gpu).data, status=status.HTTP_200_OK)

        gpuSerializer = GPUSerializer(data=gpuData)

        if gpuSerializer.is_valid() != True:
            return Response(gpuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        gpuInstance = gpuSerializer.save()

        priceData = {
            'GPUId': gpuInstance.id,
            'country': 'US',
            'available': True,
            'price': getPrice(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        priceSerializer = GPUPriceSerializer(data=priceData)

        if priceSerializer.is_valid():
            priceSerializer.save()
        
        return Response(gpuSerializer.data, status=status.HTTP_201_CREATED)


        