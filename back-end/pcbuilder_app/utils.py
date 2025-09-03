import re
import math

# This file has helper methods to get the data from a (PCPartPicker) request to match our DB structure.
# all methods generally return the found match (in an appropriate data type for the DB) or None otherwise.
#Note if you can get get price and getbuylink in 1 function

# Regex patterns
cpuModelPattern = re.compile(r'\d{3,5}\w{0,3}', re.IGNORECASE) # e.g. 7800X3D, 245K, 14700
gpuModelPrefixPattern = re.compile(r'(RTX|GTX|RX|Arc)', re.IGNORECASE)
gpuModelPattern = re.compile(rf'({gpuModelPrefixPattern.pattern})\s(\w{4})(\s(Ti SUPER|Ti|SUPER|XTX|XT))?', 
re.IGNORECASE) # e.g. RTX 4060 Ti SUPER, RX 6600
numberPattern = re.compile(r'\d+')
decimalNumberPattern = re.compile(r'\d+([.]\d+)?')
gpuNamePattern = re.compile(r'(.+?)(GeForce|Radeon|Arc)', re.IGNORECASE) # e.g. SHADOW 3X OC GeForce 
storageNamePattern = re.compile(rf'(.+?)({decimalNumberPattern.pattern})\s(TB|GB)', re.IGNORECASE) # e.g. Caviar Blue 
                                                                                                   # 4.096 TB
storageFormFactorPattern = re.compile(r'(3.5|2.5|M.2|PCIe)', re.IGNORECASE)
storageSizePattern = re.compile(rf'({decimalNumberPattern.pattern})\s(TB)', re.IGNORECASE)
casePSUWattagePattern = re.compile(rf'({numberPattern.pattern})\s(W)', re.IGNORECASE)
psuPowerPattern = re.compile(rf'(.+?)({casePSUWattagePattern.pattern})', re.IGNORECASE)
psuEfficiencyPattern = re.compile(r'(80[+])\s(Bronze|Silver|Gold|Platinum|Diamond)', re.IGNORECASE)
coolerNamePattern = re.compile(rf'(.+?)({decimalNumberPattern.pattern})\s(CFM)', re.IGNORECASE)
coolerTypePattern = re.compile(r'(Yes|No)', re.IGNORECASE)
coolerWidthPattern = re.compile(rf'({numberPattern.pattern})\s(mm)', re.IGNORECASE)
ramNamePattern = re.compile(rf'(.+?)({numberPattern.pattern})\s(GB)', re.IGNORECASE)
ramModulePattern = re.compile(rf'({numberPattern.pattern})\s(x)\s({numberPattern.pattern})(GB)', re.IGNORECASE)
ramTypePattern = re.compile(r'(DDR2|DDR3|DDR4|DDR5|DDR)', re.IGNORECASE)
ramSpeedPattern = re.compile(rf'({ramTypePattern.pattern})(-)({numberPattern.pattern})', re.IGNORECASE)
caseNamePattern = re.compile(r'(.+?)(MicroATX|ATX|Mini ITX)', re.IGNORECASE)
caseFormFactorPattern = re.compile(r'(Full Tower|Mid Tower|Mini Tower|Tower|Desktop)', re.IGNORECASE)
caseExpansionSlotPattern = re.compile(rf'({numberPattern.pattern})\s(x)\s(Full-Height|Full-Height via Riser)', re.IGNORECASE)
caseDimensionsPattern = re.compile(rf'({decimalNumberPattern.pattern})\smm\sx\s'
    rf'({decimalNumberPattern.pattern})\smm\sx\s'
    rf'({decimalNumberPattern.pattern})\smm', re.IGNORECASE)
caseDriveBayPattern = re.compile(rf'({numberPattern.pattern})\s(x)\s(Internal)\s({wantedDriveBay})', re.IGNORECASE)
caseMaxGPULengthPattern = re.compile(rf'{coolerWidthPattern.pattern}', re.IGNORECASE)




# General functions ----------------------------------------------------
# Abstract function to extract a pattern from a string
# takes the string to search in, the regex pattern to use, and the group to extract
# the default group=0 gets the entire match; otherwise specify which bracket you want
def extractPattern(value, pattern, group=0, cast=None):
    if value is None or pattern is None:
        return None

    result = None
    if match := re.search(pattern, str(value)): # *note the walrus operator
        result = match.group(group)
        
    return result

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

# Generic function to get numbers that don't require fancy conversions. e.g. 170W, 16 GB, etc. (Note: might be 
# replaced by getDecimalNumer)
def getNumber(numberString): 
    if numberString is None: 
        return None

    if number := extractPattern(numberString, numberPattern):
        number = int(number) # convert to int type
    return number

# The same as getNumber() but accepts decimal numbers e.g. 170.5W
def getDecimalNumber(numberString):
    if numberString is None:
        return None
        
    if decimalNumber := extractPattern(numberString, decimalNumberPattern):
        decimalNumber = float(decimalNumber)
    return decimalNumber

# Rounds to nearest 100 if number is 999 or below, rounds to nearest 1000 if number is 1000 to 99999.
def roundToNearest(number): 
    if number is None:
        return None

    if len(str(number)) > 3:
        return number // 1000 * 1000
    return number // 100 * 100

def getBuyLink(listings):
    if listings is None:
        return None

    buyLink = None
    for item in listings:
        if item.get('availability') and item.get('availability').upper() == 'IN STOCK': # safely check for availability
            buyLink = item.get('buyLink')
            break
    return buyLink

def getPrice(listings):
    if listings is None:
        return None

    price = None
    for item in listings:
        if item.get('availability') and item.get('availability').upper() == 'IN STOCK':
            if price := getDecimalNumber(item.get('price')):
                price = math.ceil(price)
            break
    return price
# ----------------------------------------------------



# CPU specific --------------------------------------
def getCPUSeries(series, manufacturer):
    if series is None or manufacturer is None:
        return None

    series = re.sub(re.escape(manufacturer), '', series, re.IGNORECASE)
    return series

def getCPUSpeed(speedInGHz): # converts GHz to MHz e.g. 5.7 GHz to 5700
    if speedInGHz is None:
        return None
    
    if speedInMHz := getDecimalNumber(speedInGHz):
        speedInMHz = int(speedInMHz * 1000)
    return speedInMHz

def getCPUCacheSize(L2Cache, L3Cache):
    if L2Cache is None or L3Cache is None:
        return None

    totalCache = 0
    for cache in [L2Cache, L3Cache]:
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

def getGPUBrand(name):
    if name is None:
        return None
    
    brand = None
    prefix = extractPattern(name, gpuModelPrefixPattern).upper()#////
    
    if prefix == 'RTX' or prefix == 'GTX':
        brand = 'NVIDIA'
    elif prefix == 'RX':
        brand = 'AMD'
    elif prefix == 'ARC':
        brand = 'INTEL'
        
    return brand
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
    if extractPattern(sizeString, storageSizePattern): # if storage is in terabytes; conver it to gigabytes
        size *= 1000

    size = int(size) #////
    return size
# ----------------------------------------------------



# PSU specific --------------------------------------
def getPSUName(name, manufacturer):
    if name is None or manufacturer is None:
        return None

    name = re.sub(re.escape(manufacturer), '', name, re.IGNORECASE)
    name = extractPattern(name, psuPowerPattern, 1)
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

    height = getNumber(height)
    if isLiquidCooler(type) == False and height == 0: # air coolers must have a height
        height = None
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

    type = extractPattern(type, caseNamePattern, 2)
    return type

def getCaseFormFactor(type):
    if type is None:
        return None
    
    formFactor = extractPattern(type, caseFormFactorPattern)
    return formFactor

def getCaseExpansionSlots(expansionSlots):
    if expansionSlots is None:
        return None
    # if expansionSlots is a string instead of a list (i.e. the case has only one type of expansion slot);
    # convert it to a list
    if isinstance(expansionSlots, str):
        expansionSlots = [expansionSlots]


    regularExpansionSlots = 0
    expansionSlotsViaRiser = 0
    for slot in expansionSlots:
        if match := extractPattern(slot, caseExpansionSlotPattern):
            if match.group(3).upper() == 'FULL-HEIGHT':
                regularExpansionSlots = int(match.group(1))
            elif match.group(3).upper() == 'FULL-HEIGHT VIA RISER':
                expansionSlotsViaRiser = int(match.group(1))

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
        if match := extractPattern(dimensionType, caseDimensionsPattern): #////
            dimension = int(float(match.group(wantedDimension)))
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

def getCasePSUWattage(includedPSUWattage):
    if includedPSUWattage is None:
        return None

    if match := extractPattern(includedPSUWattage, casePSUWattagePattern):
        includedPSUWattage = int(match.group(1))
    else:
        includedPSUWattage = 0
    return includedPSUWattage

def getMaxGPULength(maxGPULength):
    if maxGPULength is None:
        return None

    if isinstance(maxGPULength, str):
        maxGPULength = [maxGPULength]

    maxGPULengthInt = None
    for gpuLength in maxGPULength:
        if match := extractPattern(gpuLength, caseMaxGPULengthPattern):
            maxGPULengthInt = int(match.group(1))
            break
    return maxGPULengthInt
