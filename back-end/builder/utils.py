import re
import math




# helper methods to get the data from a request to match our db
def getModel(name, type="CPU"):
    if name is not None:
        if type == "CPU":
            match = re.search(r'\d{3,5}\w{0,3}', name) # e.g. 7800X3D
        else:
            match = re.search(r'(RTX|GTX|RX|ARC)\s*([a-z]\d{3}|\d{3,4})(\s*(ti super|ti|super|xtx|xt))?', name, re.IGNORECASE)
        if match:
            name = match.group()
    return name


def getName(name):
    if name is not None:
        match = re.search(r'(\w+)\s+(.+?)\s+(GeForce|Radeon|Arc)', name, re.IGNORECASE)
        if match:
            name = match.group(2)
    return name


def getSeries(series):
    if series is not None:
        series = re.sub(r'(AMD|INTEL)\s*', '', series, flags=re.IGNORECASE)
    return series


def getGeneration(name, type="CPU"):
    generation = None
    if name is not None:
        model = getModel(name, type)
        match = re.search(r'\d+', model) # e.g. get number only e.g. 12400 from 12400K
        if match:
            model = int(match.group()) # convert to int type
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


def getNumber(number): # generic function to get values that don't require fancy conversions. e.g. 170 W, 16 GB, 3970 MHZ
    if number is not None:
        match = re.match(r'\d+', number)
        if match:
            number = int(match.group())
    return number


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


def getBrand(name):
    if name is not None:
        if re.search(r'RTX', name, re.IGNORECASE):
            name = 'NVIDIA'
        elif re.search(r'GTX', name, re.IGNORECASE):
            name = 'NVIDIA'
        elif re.search(r'RX', name, re.IGNORECASE):
            name = 'AMD'
        elif re.search(r'ARC', name, re.IGNORECASE):
            name = 'AMD'
    return name


def roundToNearest(number): # rounds to nears 100 if number is 999 or below, rounds to nearest 1000 if number is 1000 to 99999.
    if number is not None:
        if len(str(number)) > 3:
            return number // 1000 * 1000
        return number // 100 * 100
