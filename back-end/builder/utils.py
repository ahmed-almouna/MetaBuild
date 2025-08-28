import re
import math

# Helper methods to get the data from a (PCPartPicker) request to match our db structure.


# General functions ----------------------------------------------------
def getModel(name, type):
    if name is not None and type is not None:
        if type == "CPU":
            match = re.search(r'\d{3,5}\w{0,3}', name, re.IGNORECASE) # e.g. 7800X3D
        elif type == "GPU":
            match = re.search(r'(RTX|GTX|RX|ARC)\s(\w{3,4})(\s(ti super|ti|super|xtx|xt))?', name, re.IGNORECASE)
        if match:
            name = match.group()
    return name

def getGeneration(name, type):
    generation = None
    if name is not None and type is not None:
        model = getModel(name, type)
        match = re.search(r'\d+', model) # e.g. get number only e.g. 12400 from 12400K
        if match:
            model = int(match.group()) # convert to int type
            generation = roundToNearest(model)
    return generation

# Generic function to get values that don't require fancy conversions. e.g. 170 W, 16 GB, 3970 MHZ (Note: might be replaced by getDecimalNumer)
def getNumber(number): 
    if number is not None and number != 0:
        match = re.search(r'\d+', number)
        if match:
            number = int(match.group())
    return number

# The same as getNumber() but accepts decimal numbers e.g. 170.5 W
def getDecimalNumber(number):
    if number is not None:
        match = re.search(r'\d+([.]\d+)?', number)
        if match:
            number = float(match.group())
    return number

# Rounds to nearest 100 if number is 999 or below, rounds to nearest 1000 if number is 1000 to 99999.
def roundToNearest(number): 
    if number is not None:
        if len(str(number)) > 3:
            return number // 1000 * 1000
        return number // 100 * 100

def getBuyLink(listings):
    buyLink = None
    if listings is not None:
        for item in listings:
            if item.get('availability').lower() == 'in stock':
                buyLink = item.get('buyLink')
                break
    return buyLink

# def getPrice(lowestPrice):
#     if lowestPrice is not None:
#         lowestPrice = math.ceil(lowestPrice)
#     return lowestPrice

def getPrice(listings):
    price = None
    if listings is not None:
        for item in listings:
            if item.get('availability').lower() == 'in stock':
                price = math.ceil(item.get('price'))
                break
    return price
# ----------------------------------------------------



# CPU specific --------------------------------------
def getCPUSeries(series):
    if series is not None:
        series = re.sub(r'(AMD|INTEL)\s', '', series, re.IGNORECASE)
    return series

def getCPUSpeed(speed): # convert GHz to MHz e.g. 5.7 GHz to 5700
    if speed is not None:
        match = re.search(r'\d+([.]\d+)?', speed)
        if match:
            speed = int(float(match.group()) * 1000)
    return speed

def getCPUCacheSize(L2Cache, L3Cache): # CPU
    cacheSize = 0
    if L2Cache is not None and L3Cache is not None:
        for cache in [L2Cache, L3Cache]:
            match = re.search(r'\d+', cache)
            if match:
                cacheSize += int(match.group())
    return cacheSize
# ----------------------------------------------------



# GPU specific ---------------------------------------
def getGPUName(name): 
    if name is not None:
        match = re.search(r'(\w+)(.+)(GeForce|Radeon|Arc)', name, re.IGNORECASE)
        if match:
            name = match.group(2)
    return name

def getGPUBrand(name):
    if name is not None:
        if re.search(r'(RTX|GTX)', name, re.IGNORECASE):
            name = 'NVIDIA'
        elif re.search(r'RX', name, re.IGNORECASE):
            name = 'AMD'
        elif re.search(r'ARC', name, re.IGNORECASE):
            name = 'INTEL'
    return name
# ----------------------------------------------------



# Storage specific --------------------------------------
def getStorageName(name, manufacturer): 
    if name is not None and manufacturer is not None:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        match = re.search(r'(.+)\s(\S{1,5})\s(TB|GB)', name, re.IGNORECASE)
        if match:
            name = match.group(1)
    return name

def getStorageFormFactor(formFactor):
    if formFactor is not None:
        match = re.search(r'(3.5|2.5|M.2|PCIe)', formFactor, re.IGNORECASE)
        if match:
            formFactor = match.group()
    return formFactor

def getStorageSize(size):
    if size is not None:
        match = re.search(r'\d+([.]\d+)?\sTB', size, re.IGNORECASE)
        size = getDecimalNumber(size)
        if match: # if storage is in terabytes conver it to gigabytes e.g. if 1 TB then convert to 1000 
            size *= 1000
    return size
# ----------------------------------------------------



# PSU specific --------------------------------------
def getPSUName(name, manufacturer):
    if name is not None and manufacturer is not None:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        match = re.search(r'(.+)\s(\d{3,4})\sW', name, re.IGNORECASE)
        if match:
            name = match.group(1)
    return name

def getPSUEfficiency(efficiency):
    if efficiency is not None:
        match = re.search(r'(Bronze|Silver|Gold|Platinum|Diamond)', efficiency, re.IGNORECASE)
        if match:
            efficiency = match.group()
        else:
            efficiency = '80+'
    return efficiency
# ----------------------------------------------------



# Cooler specific --------------------------------------
def getCoolerName(name, model, manufacturer):
    if model is not None:
        name = model
    elif name is not None and manufacturer is not None:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        match = re.search(r'(.+)\s(\d+([.]\d+)?)\s(CFM)', name, re.IGNORECASE)
        if match:
            name = match.group(1)
    return name

def getCoolerType(type):
    if type is not None:
        match = re.search(r'Yes', type, re.IGNORECASE)
        if match:
            type = match.group()
    return type

def getCoolerWidth(width):
    if width is not None:
        match = re.search(r'(\d{3})(\smm)', width, re.IGNORECASE)
        if match:
            width = int(match.group(1))
        else:
            width = 0
    return width
# ----------------------------------------------------



# RAM specific --------------------------------------
def getRAMName(name, manufacturer):
    if name is not None and manufacturer is not None:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        match = re.search(r'(.+?)\s(\d+)\s(GB)', name, re.IGNORECASE)
        if match:
            name = match.group(1)
    return name

def getRAMSize(Modules):
    if Modules is not None:
        match = re.search(r'(\d+)\s(x)\s(\d+)', Modules, re.IGNORECASE)
        if match:
            Modules = int(match.group(3))
    return Modules

def getRAMType(type):
    if type is not None:
        match = re.search(r'(DDR2|DDR3|DDR4|DDR5|DDR)', type, re.IGNORECASE)
        if match:
            type = match.group()
    return type

def getRAMSpeed(speed):
    if speed is not None:
        match = re.search(r'(DDR2|DDR3|DDR4|DDR5|DDR)(-)(\d+)', speed, re.IGNORECASE)
        if match:
            speed = int(match.group(3))
    return speed
# ----------------------------------------------------



# Case specific --------------------------------------
def getCaseName(name, manufacturer):
    if name is not None and manufacturer is not None:
        name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
        match = re.search(r'(.+)\s(MicroATX|ATX|Mini ITX)', name, re.IGNORECASE)
        if match:
            name = match.group(1)
    return name

def getCaseType(type):
    if type is not None:
        match = re.search(r'(MicroATX|ATX|Mini ITX)', type, re.IGNORECASE)
        if match:
            type = match.group()
    return type

def getCaseFormFactor(type):
    if type is not None:
        match = re.search(r'(Full Tower|Mid Tower|Mini Tower|Tower|Desktop)', type, re.IGNORECASE)
        if match:
            type = match.group()
    return type

def getCaseExpansionSlots(expansionSlots):
    if expansionSlots is not None:
        # if expansionSlots is a string instead of a list (i.e. the case has only one type of expansion slots), convert it to a list
        if isinstance(expansionSlots, str):
            expansionSlots = [expansionSlots]

        for expansionSlotType in expansionSlots:
            match = re.search(r'(\d+)\s(x)\s(Full-Height|Full-Height via Riser)$', expansionSlotType, re.IGNORECASE)
            if match:
                expansionSlots = int(match.group(1))
                break
    return expansionSlots

def getCaseDimensions(caseDimensions, wantedDimension): # dimensions' format is Length x Width x Height
    if caseDimensions is not None and wantedDimension is not None:
        wantedDimensionMap = {
            'length': 1,
            'width': 2,
            'height': 3
        }

        if isinstance(caseDimensions, str):
            caseDimensions = [caseDimensions]

        for caseDimensionType in caseDimensions:
            match = re.search(r'(\d+(?:[.]\d+)?)\smm\sx\s(\d+(?:[.]\d+)?)\smm\sx\s(\d+(?:[.]\d+)?)\smm', caseDimensionType, re.IGNORECASE)
            if match:
                wantedDimension = math.ceil(float(match.group(wantedDimensionMap.get(wantedDimension.lower()))))
                break
    return wantedDimension

def getCaseDriveBays(driveBays, wantedDriveBay):
    numberOfDriveBays = 0
    if driveBays is not None and wantedDriveBay is not None:

        if isinstance(driveBays, str):
            driveBays = [driveBays]

        for driveBayType in driveBays:
            match = re.search(rf'(\d+)\s(x)\s(Internal)\s({wantedDriveBay})', driveBayType, re.IGNORECASE)
            if match:
                numberOfDriveBays = int(match.group(1))
                break
    return numberOfDriveBays

def getCasePSUWattage(includedPSUWattage):
    if includedPSUWattage is not None:
        match = re.search(r'(\d+)\sW', includedPSUWattage, re.IGNORECASE)
        if match:
            includedPSUWattage = int(match.group(1))
        else:
            includedPSUWattage = 0
    return includedPSUWattage

def getMaxGPULength(maxGPULength):
    if maxGPULength is not None:
        if isinstance(maxGPULength, str):
            maxGPULength = [maxGPULength]

        for maxGPULengthType in maxGPULength:
            match = re.search(r'(\d+)\smm', maxGPULengthType)
            if match:
                maxGPULength = int(match.group(1))
                break
    return maxGPULength