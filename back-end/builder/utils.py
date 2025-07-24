import re
import math






# helper methods to get the data from a request to match our db
def getModel(name):
    if name is not None:
        match = re.search(r'\d{3,5}\w{0,3}', name)
        if match:
            name = match.group()
    return name

def getSeries(series):
    if series is not None:
        series = re.sub(r'(AMD|INTEL)\s*', '', series, flags=re.IGNORECASE)
    return series

def getGeneration(name):
    generation = None
    if name is not None:
        model = getModel(name)
        match = re.search(r'\d+', model) # e.g. get number only e.g. 12400 from 12400K
        if match:
            model = int(match.group())
            generation = roundToNearest(model)
    return generation

def getSpeed(speed):
    if speed is not None:
        match = re.match(r'\d+([.]\d+)?', speed)
        if match:
            speed = int(float(match.group()) * 1000)
    return speed

def getCacheSize(L2Cache, L3Cache):
    cacheSize = 0
    if L2Cache is not None and L3Cache is not None:
        for cache in [L2Cache, L3Cache]:
            match = re.match(r'\d+', cache)
            if match:
                cacheSize += int(match.group())
    return cacheSize

def getWattage(wattage):
    if wattage is not None:
        match = re.match(r'\d+', wattage)
        if match:
            wattage = int(match.group())
    return wattage

def getBuyLink(listings):
    buyLink = None
    if listings is not None:
        for item in listings:
            if item.get('availability') == 'In stock':
                buyLink = item.get('buyLink')
                break
    return buyLink

def getPrice(lowestPrice):
    if lowestPrice is not None:
        lowestPrice = math.ceil(lowestPrice)
    return lowestPrice

    
def roundToNearest(number): # rounds to nears 100 if number is 999 or below, rounds to nearest 1000 if number is 1000 to 99999.
    if number is not None:
        if len(str(number)) > 3:
            return number // 1000 * 1000
        return number // 100 * 100
