from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from .utils.constraints import *

# This file contains the db's models.

class CPU(models.Model):
    pcPartPickerId = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    brand          = models.CharField(choices=CPUBrands.choices)                 
    series         = models.CharField(choices=CPUSeries.choices)                 
    model          = models.CharField(max_length=kGenericMaxLength, unique=True) # e.g. 7800X
    generation     = models.PositiveIntegerField()                               # e.g. 7000
    architecture   = models.CharField(choices=CPUArchitectures.choices)          
    socket         = models.CharField(choices=Sockets.choices)
    coreCount      = models.IntegerField(choices=EvenCounts.choices)             # effeciency cores + performance cores
    threadCount    = models.IntegerField(choices=EvenCounts.choices)
    boostClock     = models.IntegerField(validators=[MinValueValidator(kMinCPUBoostClock), MaxValueValidator(kMaxCPUBoostClock)]) # in MHz
    cacheSize      = models.IntegerField(validators=[MinValueValidator(kMinCPUCacheSize), MaxValueValidator(kMaxCPUCacheSize)])   # L2 + L3, in megabytes
    tdp            = models.IntegerField(validators=[MinValueValidator(kMinCPUTDP), MaxValueValidator(kMaxCPUTDP)])               # i.e. wattage
    integratedGPU  = models.CharField(choices=CPUGraphics.choices)               
    coolerIncluded = models.BooleanField()
    rating         = models.PositiveIntegerField(null=True, blank=True)          # personal rating

    def __str__(self):
        return f"{self.series} {self.model}"


class GPU(models.Model):
    pcPartPickerId      = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    brand               = models.CharField(choices=GPUBrands.choices)                 
    manufacturer        = models.CharField(max_length=kGenericMaxLength)              # e.g. Asus
    name                = models.CharField(max_length=kGenericMaxLength)              # e.g. Ventus 2X
    model               = models.CharField(max_length=kGenericMaxLength, unique=True) # e.g. RTX 3060, RTX 3060 Ti
    series              = models.PositiveIntegerField()                               # e.g. 3000, this is like what generation is to CPU
    vramSize            = models.IntegerField(choices=EvenCounts.choices)             # in Gigabytes
    vramType            = models.CharField(choices=GPUVRAMTypes.choices)
    boostClock          = models.IntegerField(validators=[MinValueValidator(kMinGPUBoostClock), MaxValueValidator(kMaxGPUBoostClock)])
    length              = models.IntegerField(validators=[MinValueValidator(kMinGPULength), MaxValueValidator(kMaxGPULength)]) # in mm
    expansionSlots      = models.IntegerField(validators=[MinValueValidator(kMinGPUExpansionSlots), MaxValueValidator(kMaxGPUExpansionSlots)])
    pciePowerConnectors = models.CharField(choices=GPUPowerConnectors.choices)
    tdp                 = models.IntegerField(validators=[MinValueValidator(kMinGPUTDP), MaxValueValidator(kMaxGPUTDP)])
    rating              = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.model}"


class Mobo(models.Model): #Note///////////////////
    pcPartPickerId = models.CharField(max_length=kGenericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=kGenericMaxLength)
    name = models.CharField(max_length=kGenericMaxLength, unique=True)
    formFactor = models.CharField(max_length=kGenericMaxLength)
    socket = models.CharField(max_length=kGenericMaxLength)
    chipset = models.CharField(max_length=kGenericMaxLength)
    memoryType = models.CharField(max_length=kGenericMaxLength)
    memorySlots = models.PositiveIntegerField()
    memorySpeed = models.PositiveIntegerField()  # max memory speed supported
    mDotTwoSlots = models.PositiveIntegerField() # number of
    sataSlots = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name}"


class RAM(models.Model):
    pcPartPickerId = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    manufacturer   = models.CharField(max_length=kGenericMaxLength)
    name           = models.CharField(max_length=kGenericMaxLength)
    count          = models.IntegerField(choices=RAMCount.choices) # number of sticks
    size           = models.IntegerField(choices=RAMSize.choices)  # size per stick
    type           = models.CharField(choices=RAMTypes.choices)                              
    speed          = models.IntegerField(validators=[MinValueValidator(kMinRAMSpeed), MaxValueValidator(kMaxRAMSpeed)])                                            

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'count', 'size'], name='unique_ram_name_count_size')
        ]
    def __str__(self):
        return f"{self.name} {self.count} x {self.size}"


class Cooler(models.Model):
    pcPartPickerId   = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    manufacturer     = models.CharField(max_length=kGenericMaxLength)    # e.g. Cooler Master
    name             = models.CharField(max_length=kGenericMaxLength) 
    supportedSockets = ArrayField(models.CharField(max_length=kGenericMaxLength), validators=[validateCoolerSockets]) #/// see if validator works
    isLiquid         = models.BooleanField()
    height           = models.PositiveIntegerField()                             # mostly for air coolers
    width            = models.IntegerField(choices=CoolerWidths.choices) # only for liquid coolers
    rating           = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'height', 'width'], name='unique_cooler_name_height_width') # some coolers
            # have the same model name for different variants e.g. 'Aqua Elite V3' for the 120, 240, and 360 mm versions
        ]
    def __str__(self):
        return f"{self.name}"


class PSU(models.Model):
    pcPartPickerId         = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    manufacturer           = models.CharField(max_length=kGenericMaxLength)
    name                   = models.CharField(max_length=kGenericMaxLength)
    wattage                = models.IntegerField(validators=[MinValueValidator(kMinPSUWattage), MaxValueValidator(kMaxPSUWattage)])
    isModular              = models.BooleanField()
    efficiency             = models.CharField(choices=PSUEfficiencies.choices)
    formFactor             = models.CharField(choices=PSUFormFactors.choices)
    cpu8PinConnectors      = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    gpu16PinConnectors     = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    gpu12PinConnectors     = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    gpu8PinConnectors      = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    gpu6Plus2PinConnectors = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    gpu6PinConnectors      = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])
    sataConnectors         = models.IntegerField(validators=[MinValueValidator(kMinPowerConnectors), MaxValueValidator(kMaxPowerConnectors)])

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'wattage'], name='unique_psu_name_wattage')
        ]
    def __str__(self):
        return f"{self.name} {self.wattage}W"


class Storage(models.Model):
    pcPartPickerId = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)]) 
    manufacturer   = models.CharField(max_length=kGenericMaxLength)
    name           = models.CharField(max_length=kGenericMaxLength)
    size           = models.IntegerField(validators=[MinValueValidator(kMinStorageSize), MaxValueValidator(kMaxStorageSize)])
    isSSD          = models.BooleanField()
    formFactor     = models.CharField(choices=StorageFormFactors.choices) 
    cacheSize      = models.IntegerField(validators=[MinValueValidator(kMinStorageCacheSize), MaxValueValidator(kMaxStorageCacheSize)]) # in MB
    isNVMe         = models.BooleanField() # for SSDs

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'size'], name='unique_storage_name_size')
        ]
    def __str__(self):
        return f"{self.name} {self.size} GB"


class Case(models.Model):
    pcPartPickerId          = models.CharField(unique=True, validators=[MinLengthValidator(kPPPIdLength), MaxLengthValidator(kPPPIdLength)])
    manufacturer            = models.CharField(max_length=kGenericMaxLength)
    name                    = models.CharField(max_length=kGenericMaxLength, unique=True)
    type                    = models.CharField(choices=CaseTypes.choices)
    formFactor              = models.CharField(choices=CaseFormFactors.choices)
    moboFormFactors         = ArrayField(models.CharField(max_length=kGenericMaxLength), validators=[validateCaseMoboFormFactors])
    maxGPULength            = models.IntegerField(validators=[MinValueValidator(kMinCaseGPULength), MaxValueValidator(kMaxCaseGPULength)])
    expansionSlots          = models.IntegerField(validators=[MinValueValidator(kMinCaseExpansionSlots), MaxValueValidator(kMaxCaseExpansionSlots)])
    expansionSlotsViaRiser  = models.IntegerField(validators=[MinValueValidator(kMinCaseExpansionSlots), MaxValueValidator(kMaxCaseExpansionSlots)])
    height                  = models.IntegerField(validators=[MinValueValidator(kMinCaseDimensions), MaxValueValidator(kMaxCaseDimensions)])         # how tall when the case is placed in its correct orientation
    width                   = models.IntegerField(validators=[MinValueValidator(kMinCaseDimensions), MaxValueValidator(kMaxCaseDimensions)])         # the shorter side of the 2 other dimensions
    length                  = models.IntegerField(validators=[MinValueValidator(kMinCaseDimensions), MaxValueValidator(kMaxCaseDimensions)])         # the longer side of the 2 other dimensions
    threePointFiveDriveBays = models.IntegerField(validators=[MinValueValidator(kMinCaseDriveBays), MaxValueValidator(kMaxCaseDriveBays)])
    twoPointFiveDriveBays   = models.IntegerField(validators=[MinValueValidator(kMinCaseDriveBays), MaxValueValidator(kMaxCaseDriveBays)])
    includedPSUWattage      = models.IntegerField(validators=[MinValueValidator(kMinIncludedPSUWattage), MaxValueValidator(kMaxIncludedPSUWattage)]) # wattage of included PSU, can be "none"

    def __str__(self):
        return f"{self.name}"


# Price models

# Abstract model for price tables
class PartPrice(models.Model):
    country = models.CharField(choices=Countries.choices)
    price   = models.PositiveIntegerField(validators=[MinValueValidator(kMinPrice), MaxValueValidator(kMaxPrice)])
    buyLink = models.URLField(max_length=kLongMaxLength)

    class Meta:
        abstract = True

# Used to store the price of CPUs, each CPU ideally has 1 price per country
class CPUPrice(PartPrice):
    CPUId = models.ForeignKey(CPU, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CPUId', 'country'], name='unique_cpu_country_price') # 1 price per CPU per country
        ]
    def __str__(self):
        return f"{self.CPUId} ({self.country})"


class GPUPrice(PartPrice):
    GPUId = models.ForeignKey(GPU, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['GPUId', 'country'], name='unique_gpu_country_price')
        ]
    def __str__(self):
        return f"{self.GPUId} ({self.country})"


class RAMPrice(PartPrice):
    RAMId = models.ForeignKey(RAM, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['RAMId', 'country'], name='unique_ram_country_price')
        ]
    def __str__(self):
        return f"{self.RAMId} ({self.country})"


class CoolerPrice(PartPrice):
    CoolerId = models.ForeignKey(Cooler, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CoolerId', 'country'], name='unique_cooler_country_price')
        ]
    def __str__(self):
        return f"{self.CoolerId} ({self.country})"


class PSUPrice(PartPrice):
    PSUId = models.ForeignKey(PSU, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['PSUId', 'country'], name='unique_psu_country_price')
        ]
    def __str__(self):
        return f"{self.PSUId} ({self.country})"


class StoragePrice(PartPrice):
    StorageId = models.ForeignKey(Storage, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['StorageId', 'country'], name='unique_storage_country_price')
        ]
    def __str__(self):
        return f"{self.StorageId} ({self.country})"


class CasePrice(PartPrice):
    CaseId = models.ForeignKey(Case, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CaseId', 'country'], name='unique_case_country_price')
        ]
    def __str__(self):
        return f"{self.CaseId} ({self.country})"