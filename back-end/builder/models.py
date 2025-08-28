from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint

#NOTE: you might want to have all the price tables belon to a abstract table to avoid duplication.
# consider limiting options e.g. choices for countries

# Database's Models.
genericMaxLength = 100
longMaxLength = 500    # for generic string that might be bigger than 100 characters long e.g. links


class CPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    brand = models.CharField(max_length=genericMaxLength)                        # e.g. AMD
    series = models.CharField(max_length=genericMaxLength)                       # e.g. Ryzen 5
    model = models.CharField(max_length=genericMaxLength, unique=True)           # e.g. 7800X
    generation = models.PositiveIntegerField()                                   # e.g. 7000
    architecture = models.CharField(max_length=genericMaxLength)                 # e.g. Zen 5
    socket = models.CharField(max_length=genericMaxLength)
    coreCount = models.PositiveIntegerField()                                    # effeciency cores + performance cores
    threadCount = models.PositiveIntegerField()
    boostClock = models.PositiveIntegerField()
    cacheSize = models.PositiveIntegerField()                                    # L2 + L3
    tdp = models.PositiveIntegerField()                                          # i.e. wattage
    integratedGPU = models.CharField(max_length=genericMaxLength)                # can be specific model or none
    coolerIncluded = models.BooleanField()
    rating = models.PositiveIntegerField(null=True, blank=True)                  # personal rating

    def __str__(self):
        return f"{self.model}"

# Used to store the price of CPUs (each CPU has multiple prices 1 in each country)
class CPUPrice(models.Model):
    CPUId = models.ForeignKey(CPU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CPUId', 'country'], name='unique_cpu_country_price') # 1 price per CPU per country
        ]
    def __str__(self):
        return f"{self.CPUId} ({self.country})"



class GPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    brand = models.CharField(max_length=genericMaxLength)                   # e.g. Nvidia
    manufacturer = models.CharField(max_length=genericMaxLength)            # e.g. Gigabyte
    name = models.CharField(max_length=genericMaxLength)                    # e.g. Ventus 2X
    model = models.CharField(max_length=genericMaxLength, unique=True)      # e.g. RTX 3060, RTX 3060 Ti
    series = models.CharField(max_length=genericMaxLength)          # e.g. 3000 *this is like what generation is to CPU
    vramSize = models.PositiveIntegerField()
    vramType = models.CharField(max_length=genericMaxLength)
    boostClock = models.PositiveIntegerField()
    length = models.PositiveIntegerField()                                  # in mm
    expansionSlots = models.PositiveIntegerField()
    pciePowerConnectors = models.CharField(max_length=genericMaxLength)     # e.g. 1x 8-pin, 2x 6-pin, can also be None
    tdp = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.model}"

class GPUPrice(models.Model):
    GPUId = models.ForeignKey(GPU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['GPUId', 'country'], name='unique_gpu_country_price')
        ]
    def __str__(self):
        return f"{self.GPUId.model} ({self.country})"



class Mobo(models.Model): #Note///////////////////
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength, unique=True)
    formFactor = models.CharField(max_length=genericMaxLength)
    socket = models.CharField(max_length=genericMaxLength)
    chipset = models.CharField(max_length=genericMaxLength)
    memoryType = models.CharField(max_length=genericMaxLength)
    memorySlots = models.PositiveIntegerField()
    memorySpeed = models.PositiveIntegerField()  # max memory speed supported
    mDotTwoSlots = models.PositiveIntegerField() # number of
    sataSlots = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name}"


class RAM(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength)
    count = models.PositiveIntegerField()                                       # number of sticks e.g. 1, 2, 4
    size = models.PositiveIntegerField()                                        # per stick
    type = models.CharField(max_length=genericMaxLength)                        # e.g. DDR4, DDR5
    speed = models.PositiveIntegerField()                                       

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'count', 'size'], name='unique_ram_name_count_size')
        ]
    def __str__(self):
        return f"{self.name} {self.count} x {self.size}"

class RAMPrice(models.Model):
    RAMId = models.ForeignKey(RAM, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['RAMId', 'country'], name='unique_ram_country_price')
        ]
    def __str__(self):
        return f"{self.RAMId} ({self.country})"



class Cooler(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)                # e.g. Cooler Master
    name = models.CharField(max_length=genericMaxLength) 
    supportedSockets = ArrayField(models.CharField(max_length=genericMaxLength))
    isLiquid = models.BooleanField()
    height = models.PositiveIntegerField()                                      # in mm
    width = models.PositiveIntegerField()                                       # only for water coolers
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'height', 'width'], name='unique_cooler_name_height_width') # some coolers
            # have the same model name for different variants e.g. 'Aqua Elite V3' for the 120, 240, and 360 mm versions
        ]
    def __str__(self):
        return f"{self.name}"

class CoolerPrice(models.Model):
    CoolerId = models.ForeignKey(Cooler, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CoolerId', 'country'], name='unique_cooler_country_price')
        ]
    def __str__(self):
        return f"{self.CoolerId} ({self.country})"



class PSU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength, unique=True)
    wattage = models.PositiveIntegerField()
    isModular = models.BooleanField()
    efficiency = models.CharField(max_length=genericMaxLength)
    formFactor = models.CharField(max_length=genericMaxLength)
    cpu8PinConnectors = models.PositiveIntegerField()
    gpu16PinConnectors = models.PositiveIntegerField()
    gpu12PinConnectors = models.PositiveIntegerField()
    gpu8PinConnectors = models.PositiveIntegerField()
    gpu6Plus2PinConnectors = models.PositiveIntegerField()
    gpu6PinConnectors = models.PositiveIntegerField()
    sataConnectors = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} {self.wattage}W"

class PSUPrice(models.Model):
    PSUId = models.ForeignKey(PSU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['PSUId', 'country'], name='unique_psu_country_price')
        ]
    def __str__(self):
        return f"{self.PSUId} ({self.country})"



class Storage(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True) 
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength)
    size = models.PositiveIntegerField()                                        # in GB
    isSSD = models.BooleanField()
    formFactor = models.CharField(max_length=genericMaxLength)                  # e.g. M.2, 2.5, 3.5
    cacheSize = models.PositiveIntegerField()                                   # in MB
    isNVMe = models.BooleanField()                                              # for SSDs

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'size'], name='unique_storage_name_size')
        ]
    def __str__(self):
        return f"{self.name} {self.size} GB"

class StoragePrice(models.Model):
    StorageId = models.ForeignKey(Storage, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['StorageId', 'country'], name='unique_storage_country_price')
        ]
    def __str__(self):
        return f"{self.StorageId} ({self.country})"
    


class Case(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength, unique=True)
    type = models.CharField(max_length=genericMaxLength)                        # e.g. ATX, micro ATX, mini ITX
    formFactor = models.CharField(max_length=genericMaxLength)                  # e.g. full tower, mid tower, mini tower
    moboFormFactors = ArrayField(models.CharField(max_length=genericMaxLength)) # supported mobo form factors
    maxGPULength = models.PositiveIntegerField()
    expansionSlots = models.PositiveIntegerField()
    height = models.PositiveIntegerField()                 # how tall when the case is placed in its correct orientation
    width = models.PositiveIntegerField()                                   # the shorter side of the 2 other dimensions
    length = models.PositiveIntegerField()                                  # the longer side of the 2 other dimensions
    threePointFiveDriveBays = models.PositiveIntegerField()
    twoPointFiveDriveBays = models.PositiveIntegerField()
    includedPSUWattage = models.PositiveIntegerField()                          # wattage of included PSU or none

    def __str__(self):
        return f"{self.name}"

class CasePrice(models.Model):
    CaseId = models.ForeignKey(Case, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['CaseId', 'country'], name='unique_case_country_price')
        ]
    def __str__(self):
        return f"{self.CaseId} ({self.country})"
