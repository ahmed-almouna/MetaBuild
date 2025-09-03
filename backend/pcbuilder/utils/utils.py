import re
from .regex import numberPattern, decimalNumberPattern

# This file contains generic utility functions used in PCBuilder app

# Abstract function to extract a pattern from a string using regex
# Takes the string to look in, the regex pattern to look for, and the group to return
# The default group=0 returns the entire match
def extractPattern(value, pattern, group=0):
    if value is None or pattern is None:
        return None

    result = None
    if match := re.search(pattern, str(value)): # notice the walrus operator
        result = match.group(group)
        
    return result

# Generic function to get numbers that don't require fancy conversions. e.g. 170W, 16 GB, etc.
def getNumber(numberString): 
    if numberString is None: 
        return None

    if number := extractPattern(numberString, numberPattern):
        number = int(number) # convert to int type
    return number

# The same as getNumber() but also accepts decimal numbers e.g. 170.5W
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