from django.db import models
from django.core.exceptions import ValidationError

# This file contains the constraints/constants for models' fields e.g. CPU brands, VRAM types, etc.

# General constraints
kGenericMaxLength = 50
kLongMaxLength    = 1000     # for generic string that might be bigger than 100 characters long e.g. links
kPPPIdLength      = 6        # pcpartpicker Id
kMinPrice         = 0
kMaxPrice         = 2000000 # max price for a part (2M Hungarian Forint ~= $6000 usd)

 # Countries that pcpartpicker has data for
class Countries(models.TextChoices):
    australia     = "AU", "Australia"
    austria       = "AT", "Austria"
    belgium       = "BE", "Belgium"
    canada        = "CA", "Canada"
    czechRepublic = "CZ", "Czech Republic"
    denmark       = "DK", "Denmark"
    finland       = "FI", "Finland"
    france        = "FR", "France"
    germany       = "DE", "Germany"
    hungary       = "HU", "Hungary"
    ireland       = "IE", "Ireland"
    italy         = "IT", "Italy"
    netherlands   = "NL", "Netherlands"
    newZealand    = "NZ", "New Zealand"
    norway        = "NO", "Norway"
    portugal      = "PT", "Portugal"
    romania       = "RO", "Romania"
    saudiArabia   = "SA", "Saudi Arabia"
    slovakia      = "SK", "Slovakia"
    spain         = "ES", "Spain"
    sweden        = "SE", "Sweden"
    unitedKingdom = "UK", "United Kingdom"
    unitedStates  = "US", "United States"

# Common for core/thread counts, VRAM size, etc.
class EvenCounts(models.IntegerChoices):
    two         = 2, "2"
    four        = 4, "4"
    six         = 6, "6"
    eight       = 8, "8"
    ten         = 10, "10"
    eleven      = 11, "11" # RTX 2080 Ti VRAM
    twelve      = 12, "12"
    fourteen    = 14, "14"
    sixteen     = 16, "16"
    eighteen    = 18, "18"
    twenty      = 20, "20" 
    twentyTwo   = 22, "22"
    twentyFour  = 24, "24"
    twentySix   = 26, "26"
    twentyEight = 28, "28"
    thirty      = 30, "30"
    thirtyTwo   = 32, "32"
    thirtyFour  = 34, "34"
    thirtySix   = 36, "36"
    thirtyEight = 38, "38"
    forty       = 40, "40"

class Sockets(models.TextChoices):
    am4 = "AM4", "AM4"
    am5 = "AM5", "AM5"
    lga1151 = "LGA1151", "LGA1151"
    lga1200 = "LGA1200", "LGA1200"
    lga1700 = "LGA1700", "LGA1700"
    lga1851 = "LGA1851", "LGA1851"

# CPU specific ------------------------------------------------
kMinCPUBoostClock = 1000
kMaxCPUBoostClock = 10000
kMinCPUCacheSize = 2
kMaxCPUCacheSize = 250
kMinCPUTDP = 10
kMaxCPUTDP = 300

class CPUBrands(models.TextChoices):
    amd = "AMD", "AMD"
    intel = "INTEL", "Intel"

class CPUSeries(models.TextChoices):
    ryzen3 = "RYZEN 3", "Ryzen 3"
    ryzen5 = "RYZEN 5", "Ryzen 5"
    ryzen7 = "RYZEN 7", "Ryzen 7"
    ryzen9 = "RYZEN 9", "Ryzen 9"
    corei3     = "CORE I3", "Core i3"
    corei5     = "CORE I5", "Core i5"
    corei7     = "CORE I7", "Core i7"
    corei9     = "CORE I9", "Core i9"
    coreUltra5 = "CORE ULTRA 5", "Core Ultra 5"
    coreUltra7 = "CORE ULTRA 7", "Core Ultra 7"
    coreUltra9 = "CORE ULTRA 9", "Core Ultra 9"

class CPUArchitectures(models.TextChoices):
    zen     = "ZEN", "Zen"     # 1000s
    zenPlus = "ZEN+", "Zen+"   # 2000s
    zen2    = "ZEN 2", "Zen 2" # 3000s
    zen3    = "ZEN 3", "Zen 3" # 5000s
    zen4    = "ZEN 4", "Zen 4" # 7000s
    zen5    = "ZEN 5", "Zen 5" # 9000s
    coffeeLakeRefresh = "COFFEE LAKE REFRESH", "Coffee Lake Refresh" # 9000s
    cometLake         = "COMET LAKE", "Comet Lake"                   # 10,000s
    rocketLake        = "ROCKET LAKE", "Rocket Lake"                 # 11,000s
    alderLake         = "ALDER LAKE", "Alder Lake"                   # 12,000s
    raptorLake        = "RAPTOR LAKE", "Raptor Lake"                 # 13,000s
    raptorLakeRefresh = "RAPTOR LAKE REFRESH", "Raptor Lake Refresh" # 14,000s
    arrowLake         = "ARROW LAKE", "Arrow Lake"                   # 200s (Core Ultra)

class CPUGraphics(models.TextChoices):
    none = "NONE", "None"
    radeon       = "RADEON", "Radeon"                     
    radeon740M   = "RADEON 740M", "Radeon 740M"           
    radeon760M   = "RADEON 760M", "Radeon 760M"           
    radeon780M   = "RADEON 780M", "Radeon 780M"           
    radeonVega7  = "RADEON VEGA 7", "Radeon Vega 7"       
    radeonVega8  = "RADEON VEGA 8", "Radeon Vega 8"       
    radeonVega11 = "RADEON VEGA 11", "Radeon Vega 11"  
    hdGraphics630  = "INTEL HD GRAPHICS 630", "HD Graphics 630"  
    uhdGraphics630 = "INTEL UHD GRAPHICS 630", "UHD Graphics 630"
    uhdGraphics730 = "INTEL UHD GRAPHICS 730", "UHD Graphics 730"
    uhdGraphics750 = "INTEL UHD GRAPHICS 750", "UHD Graphics 750"
    uhdGraphics770 = "INTEL UHD GRAPHICS 770", "UHD Graphics 770"
    intelXe        = "INTEL XE", "Intel Xe"   
# ------------------------------------------------------


# GPU specific ------------------------------------------------
btfConnector = "GC-HPWR" # back-to-the-future connector
kMinGPUBoostClock = 500
kMaxGPUBoostClock = 5000
kMinGPULength = 100
kMaxGPULength = 500
kMinGPUExpansionSlots = 1
kMaxGPUExpansionSlots = 8
kMinGPUTDP = 10
kMaxGPUTDP = 1000

class GPUBrands(models.TextChoices):
    amd = "AMD", "AMD"
    nvidia = "NVIDIA", "Nvidia"
    intel = "INTEL", "Intel"

class GPUVRAMTypes(models.TextChoices):
    gddr6  = "GDDR6", "GDDR6"
    gddr6x = "GDDR6X", "GDDR6X"
    gddr7  = "GDDR7", "GDDR7"

class GPUPowerConnectors(models.TextChoices):
    none           = "NONE", "None"
    one6Pin        = "1 X 6-PIN", "1 x 6-pin"
    one8Pin        = "1 X 8-PIN", "1 x 8-pin"
    one8PinOne6Pin = "1 X 8-PIN + 1 X 6-PIN", "1 x 8-pin + 1 x 6-pin"
    two8Pin        = "2 X 8-PIN", "2 x 8-pin"
    two8PinOne6Pin = "2 X 8-PIN + 1 X 6-PIN", "2 x 8-pin + 1 x 6-pin"
    three8Pin      = "3 X 8-PIN", "3 x 8-pin"
    one12Pin       = "1 X 12-PIN", "1 x 12-pin"
    one16Pin       = "1 X 16-PIN", "1 x 16-pin"
    two16Pin       = "2 X 16-PIN", "2 x 16-pin"
# ------------------------------------------------------


# RAM specific ------------------------------------------------
kMinRAMSpeed = 1000
kMaxRAMSpeed = 10000

class RAMCount(models.IntegerChoices):
    one  = 1, "1"
    two  = 2, "2"
    four = 4, "4"

class RAMSize(models.IntegerChoices):
    fourGB       = 4, "4GB"
    eightGB      = 8, "8GB"
    sixteenGB    = 16, "16GB"
    twentyFourGB = 24, "24GB"
    thirtyTwoGB  = 32, "32GB"
    fortyEightGB = 48, "48GB"
    sixtyFourGB  = 64, "64GB"

class RAMTypes(models.TextChoices):
    ddr4 = "DDR4", "DDR4"
    ddr5 = "DDR5", "DDR5"
    ddr = "DDR", "DDR" #// make sure to put data like this at the back (check other funcions in create_helpers the rely on classes in this file)
#----------------------------------------------------------


# Cooler specific ------------------------------------------------
kMinCoolerHeight = 0
kMaxCoolerHeight = 250

class CoolerWidths(models.IntegerChoices):
    zeroMM              = 0, "0 mm"
    oneHundredTwentyMM  = 120, "120 mm"
    oneHundredFortyMM   = 140, "140 mm"
    twoHundredFortyMM   = 240, "240 mm"
    twoHundredEightyMM  = 280, "280 mm"
    threeHundredSixtyMM = 360, "360 mm"
    fourHundredTwentyMM = 420, "420 mm"

def validateCoolerSockets(value):
    value = [str(socket).upper() for socket in value]  # make uppercase #// this is not actually stored as uppercase, fix it
    if not any(socket in value for socket in Sockets.values):
        raise ValidationError(f"Must support at least one of: {Sockets.values}")
# ------------------------------------------------------


# PSU specific ------------------------------------------------
kMinPSUWattage = 100
kMaxPSUWattage = 3000
kMinPowerConnectors = 0
kMaxPowerConnectors = 25

class PSUEfficiencies(models.TextChoices):
    eightyPlus = "80+", "80+"           # standard
    bronze    = "BRONZE", "Bronze"
    silver    = "SILVER", "Silver"
    gold      = "GOLD", "Gold"
    platinum  = "PLATINUM", "Platinum"
    titanium  = "TITANIUM", "Titanium"

class PSUFormFactors(models.TextChoices):
    atx = "ATX", "ATX"
    sfx = "SFX", "SFX" # small form factor
# ------------------------------------------------------


# Storage specific ------------------------------------------------
kMinStorageSize = 8
kMaxStorageSize = 40000
kMinStorageCacheSize = 0
kMaxStorageCacheSize = 10000

class StorageFormFactors(models.TextChoices):
    mDot2        = "M.2", "M.2" # for any size e.g. 2230, 2280, etc.
    twoDotFive   = "2.5", "2.5"
    threeDotFive = "3.5", "3.5"
    pcie         = "PCIE", "PCIe"
# ------------------------------------------------------


# Case specific ------------------------------------------------
kMinCaseGPULength = 0
kMaxCaseGPULength = 700
kMinCaseExpansionSlots = 0
kMaxCaseExpansionSlots = 14
kMinCaseDimensions = 50
kMaxCaseDimensions = 2000
kMinCaseDriveBays = 0
kMaxCaseDriveBays = 25
kMinIncludedPSUWattage = 0
kMaxIncludedPSUWattage = 2000

class CaseTypes(models.TextChoices):
    atx      = "ATX", "ATX"
    microATX = "MICRO ATX", "Micro ATX"
    miniITX  = "MINI ITX", "Mini ITX"

class CaseFormFactors(models.TextChoices):
    desktop   = "DESKTOP", "Desktop"
    tower     = "TOWER", "Tower"
    miniTower = "MINI TOWER", "Mini Tower"
    midTower  = "MID TOWER", "Mid Tower"
    fullTower = "FULL TOWER", "Full Tower"

class CaseMoboFormFactors(models.TextChoices): #// figure out if more need to be added
    eATX     = "EATX", "EATX"
    atx      = "ATX", "ATX"
    microATX = "MICRO ATX", "Micro ATX"
    miniITX  = "MINI ITX", "Mini ITX"

def validateCaseMoboFormFactors(value):
    value = [str(formFactor).upper() for formFactor in value]
    if not any(formFactor in value for formFactor in CaseMoboFormFactors.values):
        raise ValidationError(f"Must support at least one of: {CaseMoboFormFactors.values}")
# ------------------------------------------------------
