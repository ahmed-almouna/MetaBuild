import math
from .regex import *
from .utils import *

# This file contains functions to help convert the data from a (PCPartPicker) request to match our DB structure.
# Specifically, these functions are used by API Views that add new PC parts to the parts db.
# All functions generally return the data found (in the appropriate structure and type for the db) or None otherwise.

# General (not specific to one part) ----------------------------
def getModel(name, part):
    if name is None or part is None:
        return None

    model = None
    part = part.upper()
    if part == "CPU":
        model = extractPattern(name, cpuModelPattern)
    elif part == "GPU":
        model = extractPattern(name, gpuModelPattern)
    return model

def getGeneration(name, part):
    if name is None or part is None:
        return None

    model = getModel(name, part)
    model = getNumber(model) # e.g. get number only e.g. 12400 from 12400K
    generation = roundToNearest(model)
    return generation

def getPriceAndBuyLink(listings):
    if listings is None:
        return None

    price = None
    buyLink = None
    for item in listings:
        if item.get('availability') and item.get('availability').upper() == 'IN STOCK': # safely check for availability
            buyLink = item.get('buyLink')
            if price := getDecimalNumber(item.get('price')):
                price = math.ceil(price)
            break
    return price, buyLink
# ----------------------------------------------------


# CPU specific --------------------------------------
def getCPUSeries(series, manufacturer):
    if series is None or manufacturer is None:
        return None
    
    series = re.sub(re.escape(manufacturer), '', series, re.IGNORECASE) # escape to not treat any chrachter as regex
    return series

def getCPUSpeed(speedInGHz): # converts GHz to MHz e.g. 5.7 GHz to 5700
    if speedInGHz is None:
        return None
    
    if speedInMHz := getDecimalNumber(speedInGHz):
        speedInMHz = int(speedInMHz * 1000)
    return speedInMHz

def getCPUCacheSize(l2Cache, l3Cache):
    if l2Cache is None or l3Cache is None:
        return None

    totalCache = 0
    for cache in [l2Cache, l3Cache]:
        if parsedCache := getNumber(cache):
            totalCache += parsedCache
        else:
            return None 
    return totalCache
# ----------------------------------------------------


# GPU specific ---------------------------------------
def getGPUName(name, manufacturer): 
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, gpuNamePattern, 1)
    return name

def getGPUBrand(chipset): # chipset is something like 'Radeon RX 9070 XT'
    if chipset is None:
        return None
    
    brand = None
    prefix = extractPattern(chipset, gpuModelPrefixPattern).upper()
    
    if prefix == 'RTX' or prefix == 'GTX':
        brand = 'NVIDIA'
    elif prefix == 'RX':
        brand = 'AMD'
    elif prefix == 'ARC':
        brand = 'Intel'
        
    return brand

def getGPUPCIePowerConnectors(pciePowerConnectors):
    if pciePowerConnectors is None:
        return None
    
    pciePowerConnectors = re.sub(('PCIe '), '', pciePowerConnectors, re.IGNORECASE)
    return pciePowerConnectors
# ----------------------------------------------------


# Storage specific --------------------------------------
def getStorageName(name, manufacturer): 
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, storageNamePattern, 1)
    return name

def getStorageFormFactor(formFactor):
    if formFactor is None:
        return None

    formFactor = extractPattern(formFactor, storageFormFactorPattern)
    return formFactor

def getStorageSize(sizeString):
    if sizeString is None:
        return None

    size = getDecimalNumber(sizeString)
    if extractPattern(sizeString, storageSizePattern): # if storage is in terabytes; convert it to gigabytes
        size *= 1000
    size = int(size)

    return size
# ----------------------------------------------------


# PSU specific --------------------------------------
def getPSUName(name, manufacturer):
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, psuNamePattern, 1)
    return name

def getPSUEfficiency(efficiency):
    if efficiency is None:
        return None

    if match := extractPattern(efficiency, psuEfficiencyPattern, 2):
        efficiency = match
    else:
        efficiency = '80+'
    return efficiency
# ----------------------------------------------------


# Cooler specific --------------------------------------
def getCoolerName(name, model, manufacturer):
    if model is not None: # some coolers have a model field included
        name = model
    elif name is None or manufacturer is None:
        return None
    else:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        name = extractPattern(name, coolerNamePattern, 1)

    return name

def isLiquidCooler(type):
    if type is None:
        return None
    
    isLiquid = None
    if match := extractPattern(type, coolerTypePattern):
        if match.upper() == 'YES':
            isLiquid = True
        elif match.upper() == 'NO':
            isLiquid = False

    return isLiquid
  
def getCoolerHeight(height, type):
    if height is None or type is None:
        return None

    height = getDecimalNumber(height)
    if isLiquidCooler(type) == False and height == 0: # air coolers must have a height
        return None
    elif height is not None:
        height = int(height)

    return height

def getCoolerWidth(type): # type contains the width of liquid coolers i.e. "Yes - 360 mm"
    if type is None:
        return None

    if isLiquidCooler(type) == False or isLiquidCooler(type) == None: # air coolers should not have a width
        return 0

    width = None
    if match := extractPattern(type, coolerWidthPattern, 1):
        width = int(match)
    return width
# ----------------------------------------------------


# RAM specific --------------------------------------
def getRAMName(name, manufacturer):
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, ramNamePattern, 1)
    return name

def getRAMModule(module, type):
    if module is None or type is None:
        return None

    result = None
    if type.upper() == 'SIZE':
        if result := extractPattern(module, ramModulePattern, 3):
            result = int(result)
    elif type.upper() == 'COUNT':
        if result := extractPattern(module, ramModulePattern, 1):
            result = int(result)
    return result

def getRAMType(type):
    if type is None:
        return None
    
    type = extractPattern(type, ramTypePattern)
    return type

def getRAMSpeed(speed):
    if speed is None:
        return None

    if speed := extractPattern(speed, ramSpeedPattern, 3):
        speed = int(speed)
    return speed
# ----------------------------------------------------


# Case specific --------------------------------------
def getCaseName(name, manufacturer):
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, caseNamePattern, 1)
    return name

def getCaseType(type):
    if type is None:
        return None

    type = extractPattern(type, caseTypePattern)
    return type

def getCaseFormFactor(type):
    if type is None:
        return None
    
    formFactor = extractPattern(type, caseFormFactorPattern)
    return formFactor

def getCaseExpansionSlots(expansionSlots):
    if expansionSlots is None:
        return None

    # if expansionSlots is a string instead of a list of strings (i.e. the case has only one type of expansion slot);
    # treat it as a list
    if isinstance(expansionSlots, str):
        expansionSlots = [expansionSlots]

    regularExpansionSlots = 0
    expansionSlotsViaRiser = 0
    for slot in expansionSlots:
        if match := extractPattern(slot, caseExpansionSlotPattern, 3):
            if match.upper() == 'FULL-HEIGHT':
                match = extractPattern(slot, caseExpansionSlotPattern, 1)
                regularExpansionSlots = int(match)
            elif match.upper() == 'FULL-HEIGHT VIA RISER':
                match = extractPattern(slot, caseExpansionSlotPattern, 1)
                expansionSlotsViaRiser = int(match)

    if regularExpansionSlots == 0 and expansionSlotsViaRiser == 0:
        return None

    return regularExpansionSlots, expansionSlotsViaRiser

def getCaseDimensions(caseDimensions, wantedDimension): # dimensions' format is Length x Width x Height
    if caseDimensions is None or wantedDimension is None:
        return None

    wantedDimensionMap = {
        'LENGTH': 1,
        'WIDTH': 2,
        'HEIGHT': 3
    }
    wantedDimension = wantedDimensionMap.get(wantedDimension.upper())
    if isinstance(caseDimensions, str):
        caseDimensions = [caseDimensions]

    dimension = None
    for dimensionType in caseDimensions:
        if match := extractPattern(dimensionType, caseDimensionsPattern, wantedDimension):
            dimension = int(float(match))
            break
    return dimension

def getCaseDriveBays(driveBays, wantedDriveBay):
    if driveBays is None or wantedDriveBay is None:
        return None

    if isinstance(driveBays, str):
        driveBays = [driveBays]

    numberOfDriveBays = 0
    for driveBay in driveBays:
        if match := re.search(rf'(\d+)\s(x)\s(Internal\s{re.escape(wantedDriveBay)})', driveBay, re.IGNORECASE):
            numberOfDriveBays = int(match.group(1))
            break
    return numberOfDriveBays

def getMaxGPULength(maxGPULengthString):
    if maxGPULengthString is None:
        return None

    if isinstance(maxGPULengthString, str):
        maxGPULengthString = [maxGPULengthString]

    maxGPULength = None
    for length in maxGPULengthString:
        if match := extractPattern(length, caseMaxGPULengthPattern, 1):
            maxGPULength = int(match)
            break
    return maxGPULength
# ------------------------------------------------------