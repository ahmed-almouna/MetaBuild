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

# Views i.e. API end-points.

# Gives a PC build.
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


# Adds a CPU to the database.
class addCPU(APIView):
    def post(self, request):
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})
        
        cpuData = {
            'pcPartPickerId': data.get('id'),
            'model': getModel(data.get('name'), type="CPU"),
            'brand': specs.get('Manufacturer'),
            'series': getSeries(specs.get('Series')),
            'generation': getGeneration(data.get('name'), type="CPU"),
            'socket': specs.get('Socket'),
            'architecture': specs.get('Microarchitecture'),
            'coreCount': specs.get('Core Count'),
            'threadCount': specs.get('Thread Count'),
            'boostClock': getSpeed(specs.get('Performance Core Boost Clock')),
            'tdp': getNumber(specs.get('TDP')),
            'cacheSize': getCPUCacheSize(specs.get('L2 Cache'), specs.get('L3 Cache')),
            'coolerIncluded': specs.get('Includes Cooler', False),
            'integratedGPU': specs.get('Integrated Graphics', "None"),
        }

        cpuSerializer = CPUSerializer(data=cpuData)

        if cpuSerializer.is_valid() != True:
            return Response(cpuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cpuInstance = cpuSerializer.save()

        priceData = {
            'CPUId': cpuInstance.id,
            'country': 'US',
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
            'name': getGPUName(data.get('name')),
            'series': getGeneration(data.get('name'), type="GPU"),
            'boostClock': getNumber(specs.get('Boost Clock')),
            'tdp': getNumber(specs.get('TDP')),
            'vramSize': getNumber(specs.get('Memory')),
            'vramType': specs.get('Memory Type'),
            'length': getNumber(specs.get('Length')),
            'expansionSlots': getNumber(specs.get('Total Slot Width')),
            'pciePowerConnectors': specs.get('External Power'),
        }

        gpuSerializer = GPUSerializer(data=gpuData)

        if gpuSerializer.is_valid() != True:
            return Response(gpuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        gpuInstance = gpuSerializer.save()

        priceData = {
            'GPUId': gpuInstance.id,
            'country': 'US',
            'price': getPrice(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        priceSerializer = GPUPriceSerializer(data=priceData)

        if priceSerializer.is_valid():
            priceSerializer.save()
        
        return Response(gpuSerializer.data, status=status.HTTP_201_CREATED)


class addStorage(APIView):
    def post(self, request):
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})
        
        storageData = {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getStorageName(data.get('name'), specs.get('Manufacturer')),
            'size': getStorageSize(specs.get('Capacity')),
            'isSSD': specs.get('Type') == 'SSD',
            'formFactor': getFormFactor(specs.get('Form Factor')),
            'cacheSize': getNumber(specs.get('Cache', 0)),
            'isNVMe': specs.get('NVME'),
        }

        storageSerializer = StorageSerializer(data=storageData)

        if storageSerializer.is_valid() != True:
            return Response(storageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        storageInstance = storageSerializer.save()

        priceData = {
            'StorageId': storageInstance.id,
            'country': 'US',
            'price': getPrice(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        priceSerializer = StoragePriceSerializer(data=priceData)

        if priceSerializer.is_valid():
            priceSerializer.save()
        
        return Response(storageSerializer.data, status=status.HTTP_201_CREATED)
        

class addPSU(APIView):
    def post(self, request):
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})
        
        psuData = {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getPSUName(data.get('name'), specs.get('Manufacturer')),
            'wattage': getNumber(specs.get('Wattage')),
            'isModular': specs.get('Modular', "No") == 'Full',
            'efficiency': getEfficiency(specs.get('Efficiency Rating', "80+")),
            'formFactor': getFormFactor(specs.get('Type', "ATX")),
            'cpu8PinConnectors': getNumber(specs.get('EPS 8-pin Connectors')),
            'gpu16PinConnectors': getNumber(specs.get('PCIe 16-pin 12VHPWR/12V-2x6 Connectors')),
            'gpu12PinConnectors': getNumber(specs.get('PCIe 12-pin Connectors')),
            'gpu8PinConnectors': getNumber(specs.get('PCIe 8-pin Connectors')),
            'gpu6Plus2PinConnectors': getNumber(specs.get('PCIe 6+2-pin Connectors')),
            'gpu6PinConnectors': getNumber(specs.get('PCIe 6-pin Connectors')),
            'sataConnectors': getNumber(specs.get('SATA Connectors')),
        }

        psuSerializer = PSUSerializer(data=psuData)

        if psuSerializer.is_valid() != True:
            return Response(psuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        psuInstance = psuSerializer.save()

        priceData = {
            'PSUId': psuInstance.id,
            'country': 'US',
            'price': getPrice(listings.get('lowestPrice')),
            'buyLink': getBuyLink(listings.get('prices'))
        }

        priceSerializer = PSUPriceSerializer(data=priceData)

        if priceSerializer.is_valid():
            priceSerializer.save()
        
        return Response(psuSerializer.data, status=status.HTTP_201_CREATED)