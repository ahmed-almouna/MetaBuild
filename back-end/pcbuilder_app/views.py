from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from .utils import *

# Site's Views i.e. API end-points i.e. URLs.

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


# Abstract view for adding parts to the database
class addPartView(APIView):
    # Must be set in the child class
    partSerializer = None
    priceSerializer = None
    partDataBuilder = None

    def post(self, request):
        # Get the API request's data
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})

        # Create a part instance from the request and save it to the DB
        partData = self.partDataBuilder(data, specs)
        partSerializer = self.partSerializer(data=partData)
        partSerializer.is_valid(raise_exception=True)
        partInstance = partSerializer.save()

        priceData = {
            f'{partInstance.__class__.__name__}Id': partInstance.id, # get the name of the model dynamically
            'country': 'US',
            'price': getPrice(listings.get('prices')),
            'buyLink': getBuyLink(listings.get('prices'))
        }
        priceSerializer = self.priceSerializer(data=priceData)
        if priceSerializer.is_valid():
            priceSerializer.save()

        return Response(partSerializer.data, status=status.HTTP_201_CREATED)


# Concrete view to add a CPU to the database.
class addCPU(addPartView):
    partSerializer = CPUSerializer
    priceSerializer = CPUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'model': getModel(data.get('name'), "CPU"),
            'brand': specs.get('Manufacturer'),
            'series': getCPUSeries(specs.get('Series'), specs.get('Manufacturer')),
            'generation': getGeneration(data.get('name'), "CPU"),
            'socket': specs.get('Socket'),
            'architecture': specs.get('Microarchitecture'),
            'coreCount': specs.get('Core Count'),
            'threadCount': specs.get('Thread Count'),
            'boostClock': getCPUSpeed(specs.get('Performance Core Boost Clock')),
            'tdp': getNumber(specs.get('TDP')),
            'cacheSize': getCPUCacheSize(specs.get('L2 Cache'), specs.get('L3 Cache')),
            'coolerIncluded': specs.get('Includes Cooler', False),
            'integratedGPU': specs.get('Integrated Graphics', "None"),
        }


class addGPU(addPartView):
    partSerializer = GPUSerializer
    priceSerializer = GPUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'model': getModel(data.get('name'), "GPU"),
            'brand': getGPUBrand(specs.get('Chipset')),
            'manufacturer': specs.get('Manufacturer'),
            'name': getGPUName(data.get('name'), specs.get('Manufacturer')),
            'series': getGeneration(data.get('name'), "GPU"),
            'boostClock': getNumber(specs.get('Boost Clock')),
            'tdp': getNumber(specs.get('TDP')),
            'vramSize': getNumber(specs.get('Memory')),
            'vramType': specs.get('Memory Type'),
            'length': getNumber(specs.get('Length')),
            'expansionSlots': getNumber(specs.get('Total Slot Width')),
            'pciePowerConnectors': specs.get('External Power'),
        }
        

class addStorage(addPartView):
    partSerializer = StorageSerializer
    priceSerializer = StoragePriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getStorageName(data.get('name'), specs.get('Manufacturer')),
            'size': getStorageSize(specs.get('Capacity')),
            'isSSD': specs.get('Type') == 'SSD',
            'formFactor': getStorageFormFactor(specs.get('Form Factor')),
            'cacheSize': getNumber(specs.get('Cache', "0")), # set it to 0 if not specified
            'isNVMe': specs.get('NVME'),
        }
        

class addPSU(addPartView):
    partSerializer = PSUSerializer
    priceSerializer = PSUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getPSUName(data.get('name'), specs.get('Manufacturer')),
            'wattage': getNumber(specs.get('Wattage')),
            'isModular': specs.get('Modular', "No") == 'Full',
            'efficiency': getPSUEfficiency(specs.get('Efficiency Rating', "80+")),
            'formFactor': specs.get('Type', "ATX"),
            'cpu8PinConnectors': getNumber(specs.get('EPS 8-pin Connectors')),
            'gpu16PinConnectors': getNumber(specs.get('PCIe 16-pin 12VHPWR/12V-2x6 Connectors')),
            'gpu12PinConnectors': getNumber(specs.get('PCIe 12-pin Connectors')),
            'gpu8PinConnectors': getNumber(specs.get('PCIe 8-pin Connectors')),
            'gpu6Plus2PinConnectors': getNumber(specs.get('PCIe 6+2-pin Connectors')),
            'gpu6PinConnectors': getNumber(specs.get('PCIe 6-pin Connectors')),
            'sataConnectors': getNumber(specs.get('SATA Connectors')),
        }


class addCooler(addPartView):
    partSerializer = CoolerSerializer
    priceSerializer = CoolerPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getCoolerName(data.get('name'), specs.get('Model'), specs.get('Manufacturer')),
            'supportedSockets': specs.get('CPU Socket'),
            'isLiquid': isLiquidCooler(specs.get('Water Cooled')),
            'height': getNumber(specs.get('Height', "0")),
            'width': getCoolerWidth(specs.get('Water Cooled', "0")),#////
        }


class addRAM(addPartView):
    partSerializer = RAMSerializer
    priceSerializer = RAMPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getRAMName(data.get('name'), specs.get('Manufacturer')),
            'count': getRAMModule(specs.get('Modules'), 'COUNT'),
            'size': getRAMModule(specs.get('Modules'), 'SIZE'),
            'type': getRAMType(specs.get('Speed')), # spped also contains type i.e. "DDR5-6000"
            'speed': getRAMSpeed(specs.get('Speed')),
        }
        

class addCase(APIView):
    partSerializer = CaseSerializer
    priceSerializer = CasePriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        expansionSlots, expansionSlotsViaRiser = getCaseExpansionSlots(specs.get('Expansion Slots'))
        return {
            'pcPartPickerId': data.get('id'),
            'manufacturer': specs.get('Manufacturer'),
            'name': getCaseName(data.get('name'), specs.get('Manufacturer')),
            'type': getCaseType(specs.get('Type')),
            'formFactor': getCaseFormFactor(specs.get('Type')),
            'moboFormFactors': specs.get('Motherboard Form Factor'), 
            'maxGPULength': getMaxGPULength(specs.get('Maximum Video Card Length')),
            'expansionSlots': expansionSlots, 
            'expansionSlotsViaRiser': expansionSlotsViaRiser, 
            'height': getCaseDimensions(specs.get('Dimensions'), 'height'),
            'width': getCaseDimensions(specs.get('Dimensions'), 'width'),
            'length': getCaseDimensions(specs.get('Dimensions'), 'length'),
            'threePointFiveDriveBays': getCaseDriveBays(specs.get('Drive Bays', []), '3.5'), 
            'twoPointFiveDriveBays': getCaseDriveBays(specs.get('Drive Bays', []), '2.5'),
            'includedPSUWattage': getCasePSUWattage(specs.get('Power Supply', "0")),#////////
        }
