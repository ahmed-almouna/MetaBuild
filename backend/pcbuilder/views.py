from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils.constraints import Countries 
from . import serializers
from .utils.create_helpers import *

# This file contains the apps's views aka API end-points aka URLs.

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


# Abstract view for adding pc parts to the db.
class AddPartView(APIView):
    # Must be set in the child class
    partSerializer = None
    priceSerializer = None
    partDataBuilder = None

    def post(self, request, format=None):
        # Get the request's data
        data = request.data
        listings = data.get('prices', {})
        specs = data.get('specifications', {})

        # Construct a part instance from the request and save it to the db
        partData = self.partDataBuilder(data, specs)
        partSerializer = self.partSerializer(data=partData)
        partSerializer.is_valid(raise_exception=True)
        partInstance = partSerializer.save()

        # Construct a price instance if it exists and save it to the db
        price, buyLink = getPriceAndBuyLink(listings.get('prices'))
        priceData = {
            f'{partInstance.__class__.__name__}Id': partInstance.id, # get the name of the model dynamically
            'country': Countries.unitedStates,
            'price'  : price,
            'buyLink': buyLink
        }
        priceSerializer = self.priceSerializer(data=priceData)
        if priceSerializer.is_valid(): # if price doesn't exist or is invalid, just ignore it
            priceSerializer.save()

        return Response(partSerializer.data, status=status.HTTP_201_CREATED)

# Concrete view to add a CPU to the db.
class AddCPU(AddPartView):
    partSerializer = serializers.CPUSerializer
    priceSerializer = serializers.CPUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId' : safeStr(data.get('id')),
            'model'          : safeStr(getModel(data.get('name'), "CPU")).upper(),
            'brand'          : safeStr(specs.get('Manufacturer')).upper(),
            'series'         : getCPUSeries(specs.get('Series')),
            'generation'     : getGeneration(data.get('name'), "CPU"),
            'socket'         : safeStr(specs.get('Socket')).upper(),
            'architecture'   : safeStr(specs.get('Microarchitecture')).upper(),
            'coreCount'      : specs.get('Core Count'),
            'threadCount'    : specs.get('Thread Count'),
            'boostClock'     : getCPUSpeed(specs.get('Performance Core Boost Clock')),
            'tdp'            : getNumber(specs.get('TDP')),
            'cacheSize'      : getCPUCacheSize(specs.get('L2 Cache'), specs.get('L3 Cache')),
            'coolerIncluded' : specs.get('Includes Cooler', False),
            'integratedGPU'  : safeStr(specs.get('Integrated Graphics', "NONE")).upper(),
        }


class AddGPU(AddPartView):
    partSerializer = serializers.GPUSerializer
    priceSerializer = serializers.GPUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        if btfConnector in safeStr(specs.get('Interface')).upper():# don't accept GPUs with BTF connectors #/// maybe you show send something different than None
            return None
        if data.get('Uses Back-Connect Connectors') == "Yes":#/// relocate this to mobo
            return None
        return {
            'pcPartPickerId'      : safeStr(data.get('id')),
            'model'               : safeStr(getModel(data.get('name'), "GPU")).upper(),
            'brand'               : safeStr(getGPUBrand(specs.get('Chipset'))).upper(),
            'manufacturer'        : safeStr(specs.get('Manufacturer')).upper(),
            'name'                : safeStr(getGPUName(data.get('name'), specs.get('Manufacturer'))).upper(),
            'series'              : getGeneration(data.get('name'), "GPU"),
            'boostClock'          : getNumber(specs.get('Boost Clock')),
            'tdp'                 : getNumber(specs.get('TDP')),
            'vramSize'            : getNumber(specs.get('Memory')),
            'vramType'            : safeStr(specs.get('Memory Type')).upper(),
            'length'              : getNumber(specs.get('Length')),
            'expansionSlots'      : getNumber(specs.get('Total Slot Width')),
            'pciePowerConnectors' : safeStr(getGPUPCIePowerConnectors(specs.get('External Power'))).upper(),
        }
        

class AddStorage(AddPartView):
    partSerializer = serializers.StorageSerializer
    priceSerializer = serializers.StoragePriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        isSSD = safeStr(specs.get('Type')).upper() == 'SSD'
        formFactor = getStorageFormFactor(specs.get('Form Factor'))
        isNVMe = specs.get('NVME')
        if storageIsValid(isSSD, formFactor, isNVMe) == False: #/// see if you can send smth more meaningful than None
            return None

        return {
            'pcPartPickerId' : safeStr(data.get('id')),
            'manufacturer'   : safeStr(specs.get('Manufacturer')).upper(),
            'name'           : safeStr(getStorageName(data.get('name'), specs.get('Manufacturer'))).upper(),
            'size'           : getStorageSize(specs.get('Capacity')),
            'isSSD'          : isSSD,
            'formFactor'     : formFactor,
            'cacheSize'      : getNumber(specs.get('Cache', "0")),
            'isNVMe'         : isNVMe,
        }
        

class AddPSU(AddPartView):
    partSerializer = serializers.PSUSerializer
    priceSerializer = serializers.PSUPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId'         : safeStr(data.get('id')),
            'manufacturer'           : safeStr(specs.get('Manufacturer')).upper(),
            'name'                   : safeStr(getPSUName(data.get('name'), specs.get('Manufacturer'))).upper(),
            'wattage'                : getNumber(specs.get('Wattage')),
            'isModular'              : 'FULL' in safeStr(specs.get('Modular')).upper(),
            'efficiency'          : getPSUEfficiency(specs.get('Efficiency Rating', PSUEfficiencies.eightyPlus.value)),
            'formFactor'             : safeStr(specs.get('Type', 'ATX')).upper(),
            'cpu8PinConnectors'      : specs.get('EPS 8-pin Connectors'),
            'gpu16PinConnectors'     : specs.get('PCIe 16-pin 12VHPWR/12V-2x6 Connectors'),
            'gpu12PinConnectors'     : specs.get('PCIe 12-pin Connectors'),
            'gpu8PinConnectors'      : specs.get('PCIe 8-pin Connectors'),
            'gpu6Plus2PinConnectors' : specs.get('PCIe 6+2-pin Connectors'),
            'gpu6PinConnectors'      : specs.get('PCIe 6-pin Connectors'),
            'sataConnectors'         : specs.get('SATA Connectors'),
        }


class AddCooler(AddPartView):
    partSerializer = serializers.CoolerSerializer
    priceSerializer = serializers.CoolerPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        return {
            'pcPartPickerId'   : safeStr(data.get('id')),
            'manufacturer'     : safeStr(specs.get('Manufacturer')).upper(),
            'name'   : safeStr(getCoolerName(data.get('name'), specs.get('Model'), specs.get('Manufacturer'))).upper(),
            'supportedSockets' : specs.get('CPU Socket'),
            'isLiquid'         : isLiquidCooler(specs.get('Water Cooled')),
            'height'           : getCoolerHeight(specs.get('Height', "0"), specs.get('Water Cooled')),
            'width'            : getCoolerWidth(specs.get('Water Cooled', "0")),
        }


class AddRAM(AddPartView):
    partSerializer = serializers.RAMSerializer
    priceSerializer = serializers.RAMPriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        if "SODIMM" in data.get('Form Factor', "").upper(): # don't accept laptop RAM #///
            return None
        return {
            'pcPartPickerId' : safeStr(data.get('id')),
            'manufacturer'   : safeStr(specs.get('Manufacturer')).upper(),
            'name'           : safeStr(getRAMName(data.get('name'), specs.get('Manufacturer'))).upper(),
            'count'          : getRAMModule(specs.get('Modules'), 'COUNT'),
            'size'           : getRAMModule(specs.get('Modules'), 'SIZE'),
            'type'           : getRAMType(specs.get('Speed')), # speed also contains type i.e. "DDR5-6000"
            'speed'          : getRAMSpeed(specs.get('Speed')),
        }
        

class AddCase(AddPartView):
    partSerializer = serializers.CaseSerializer
    priceSerializer = serializers.CasePriceSerializer

    @staticmethod
    def partDataBuilder(data, specs):
        moboFormFactors = specs.get('Motherboard Form Factor')
        if isinstance(moboFormFactors, list):
            moboFormFactors = [formFactor.upper() for formFactor in moboFormFactors]
        else:
            moboFormFactors = [moboFormFactors.upper()]
        expansionSlots, expansionSlotsViaRiser = getCaseExpansionSlots(specs.get('Expansion Slots')) #// make it so a case can have no exapnsion slots
        includedPSUWattage = getNumber(specs.get('Power Supply'))
        return {
            'pcPartPickerId'          : safeStr(data.get('id')),
            'manufacturer'            : safeStr(specs.get('Manufacturer')).upper(),
            'name'                    : safeStr(getCaseName(data.get('name'), specs.get('Manufacturer'))).upper(),
            'type'                    : getCaseType(specs.get('Type')),
            'formFactor'        : getCaseFormFactor(specs.get('Type')), # type also contains formfactor "ATX Mid Tower"
            'moboFormFactors'         : moboFormFactors, 
            'maxGPULength'            : getCaseMaxGPULength(specs.get('Maximum Video Card Length')), #// make it so a case can have no max GPU length
            'expansionSlots'          : expansionSlots, 
            'expansionSlotsViaRiser'  : expansionSlotsViaRiser, 
            'height'                  : getCaseDimensions(specs.get('Dimensions'), 'HEIGHT'),
            'width'                   : getCaseDimensions(specs.get('Dimensions'), 'WIDTH'),
            'length'                  : getCaseDimensions(specs.get('Dimensions'), 'LENGTH'),
            'threePointFiveDriveBays' : getCaseDriveBays(specs.get('Drive Bays', []), '3.5'), 
            'twoPointFiveDriveBays'   : getCaseDriveBays(specs.get('Drive Bays', []), '2.5'),
            'includedPSUWattage'      : includedPSUWattage if includedPSUWattage is not None else 0,
        }
