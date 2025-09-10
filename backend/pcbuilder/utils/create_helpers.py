import math
from .regex import *
from .utils import *
from .constraints import *

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
    model = getNumber(model) # get number only e.g. get 12400 from 12400K
    generation = roundToNearest(model)
    return generation

def getPriceAndBuyLink(listings):
    if listings is None:
        return None, None

    price = None
    buyLink = None
    for item in listings:
        if item.get('availability', "").upper() == 'IN STOCK':
            buyLink = item.get('buyLink')
            if price := getDecimalNumber(item.get('price')):
                price = math.ceil(price)
            break
    return price, buyLink
# ----------------------------------------------------


# CPU specific --------------------------------------
def getCPUSeries(series):
    if series is None:
        return None

    series = str(series).upper()
    cpuSeries = None
    for validSeries in CPUSeries.values:
        if validSeries in series:
            cpuSeries = validSeries
            break
    return cpuSeries


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

    name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
    name = extractPattern(name, gpuNamePattern, 1)
    return name

def getGPUBrand(chipset): # chipset is something like 'Radeon RX 9070 XT'
    if chipset is None:
        return None
    
    brand = None
    if prefix := extractPattern(chipset, gpuModelPrefixPattern):
        prefix = prefix.upper()
    
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
    
    pciePowerConnectors = re.sub(('PCIe '), '', str(pciePowerConnectors), re.IGNORECASE)
    return pciePowerConnectors
# ----------------------------------------------------


# Storage specific --------------------------------------
def getStorageName(name, manufacturer): 
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
    name = extractPattern(name, storageNamePattern, 1)
    return name

def getStorageFormFactor(formFactor):
    if formFactor is None:
        return None

    formFactor = str(formFactor).upper()
    storageFormFactor = None
    for validFormFactor in StorageFormFactors.values:
        if validFormFactor in formFactor:
            storageFormFactor = validFormFactor
            break
    return storageFormFactor

def getStorageSize(sizeString):
    if sizeString is None:
        return None

    size = getDecimalNumber(sizeString)
    if extractPattern(sizeString, storageSizePattern): # if storage is in terabytes; convert it to gigabytes
        size *= 1000
    if size is not None:
        size = int(size)

    return size

def storageIsValid(isSSD, formFactor, isNVMe):
    if isSSD == False and isNVMe == True:
        return False # ssd and nvme, ssd and not nvme, not ssd and not nvme

    if isSSD == False:
        if formFactor == StorageFormFactors.mDot2.value or formFactor == StorageFormFactors.pcie.value:
            return False

    return True

# ----------------------------------------------------


# PSU specific --------------------------------------
def getPSUName(name, manufacturer):
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
    name = extractPattern(name, psuNamePattern, 1)
    return name

def getPSUEfficiency(efficiency):
    if efficiency is None:
        return None

    efficiency = str(efficiency).upper()
    psuEfficiency = PSUEfficiencies.eightyPlus.value
    for validEfficiency in PSUEfficiencies.values:
        if validEfficiency in efficiency:
            psuEfficiency = validEfficiency
            break
    
    return psuEfficiency
# ----------------------------------------------------


# Cooler specific --------------------------------------
def getCoolerName(name, model, manufacturer):
    if model is not None: # some coolers have a model field included
        name = model
    elif name is None or manufacturer is None:
        return None
    else:
        name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
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

    name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
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

def getRAMType(speed):
    if speed is None:
        return None

    type = str(speed).upper()
    ramType = None
    for validType in RAMTypes.values:
        if validType in type:
            ramType = validType
            break

    return ramType

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

    name = re.sub(re.escape(str(manufacturer)), '', str(name), re.IGNORECASE)
    name = extractPattern(name, caseNamePattern, 1)
    return name

def getCaseType(type):
    if type is None:
        return None

    # replace "MicroATX" with "Micro ATX" to be consistent with mobo form factor
    type = str(type).upper()
    type = type.replace('MICROATX', 'MICRO ATX')
    
    caseType = None
    for validType in CaseTypes.values:
        if validType in type:
            caseType = validType
            break
    return caseType

def getCaseFormFactor(type):
    if type is None:
        return None
    
    type = str(type).upper()
    caseFormFactor = None
    for validFormFactor in CaseFormFactors.values:
        if validFormFactor in type:
            caseFormFactor = validFormFactor
            break
    return caseFormFactor

def getCaseExpansionSlots(expansionSlots):
    if expansionSlots is None:
        return None, None

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
        return None, None

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
        if match := re.search(rf'(\d+)\s(x)\s((Internal|External)\s{re.escape(wantedDriveBay)})', driveBay, re.IGNORECASE):
            numberOfDriveBays = int(match.group(1))
            break
    return numberOfDriveBays

def getCaseMaxGPULength(maxGPULengthString):
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