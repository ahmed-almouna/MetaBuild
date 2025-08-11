import socket
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint

# Models.

genericMaxLength = 100
longMaxLength = 500 # for generic string that might be bigger that 100 charachters long e.g. links

class CPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    brand = models.CharField(max_length=genericMaxLength) # e.g. AMD
    series = models.CharField(max_length=genericMaxLength) # e.g. Ryzen 5
    model = models.CharField(max_length=genericMaxLength, unique=True) # e.g. 7800X
    generation = models.PositiveIntegerField() # e.g. 7000
    architecture = models.CharField(max_length=genericMaxLength) # e.g. Zen 5
    socket = models.CharField(max_length=genericMaxLength)
    coreCount = models.PositiveIntegerField() # effeciency cores + performance cores
    threadCount = models.PositiveIntegerField()
    boostClock = models.PositiveIntegerField()
    cacheSize = models.PositiveIntegerField() # L2 + L3
    tdp = models.PositiveIntegerField() # i.e. wattage
    integratedGPU = models.CharField(max_length=genericMaxLength) # can be specific model or None
    coolerIncluded = models.BooleanField()
    rating = models.PositiveIntegerField(null=True, blank=True) # personal rating

    def __str__(self):
        return self.model

# Used to store the price of CPUs in (a CPU can have mutliple prices in depending on country)
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
        return self.CPUId.model


class GPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    brand = models.CharField(max_length=genericMaxLength) # e.g. Nvidia
    manufacturer = models.CharField(max_length=genericMaxLength) # e.g. Gigabyte
    name = models.CharField(max_length=genericMaxLength) # e.g. Ventus 2X
    model = models.CharField(max_length=genericMaxLength, unique=True) # e.g. RTX 3060
    series = models.CharField(max_length=genericMaxLength) # e.g. 5000, 7000 *this is like what generation is to CPU
    vramSize = models.PositiveIntegerField()
    vramType = models.CharField(max_length=genericMaxLength)
    boostClock = models.PositiveIntegerField()
    length = models.PositiveIntegerField() # in mm
    expansionSlots = models.PositiveIntegerField()
    pciePowerConnectors = models.CharField(max_length=genericMaxLength) # e.g. 1x 8-pin, 2x 6-pin, can also be None
    tdp = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.model

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
        return self.GPUId.model


class Mobo(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength, unique=True)
    formFactor = models.CharField(max_length=genericMaxLength)
    socket = models.CharField(max_length=genericMaxLength)
    chipset = models.CharField(max_length=genericMaxLength)
    memoryType = models.CharField(max_length=genericMaxLength)
    memorySlots = models.PositiveIntegerField()
    memorySpeed = models.PositiveIntegerField() # max memory speed supported
    mDotTwoSlots = models.PositiveIntegerField() # *number of
    sataSlots = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class RAM(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength)
    size = models.PositiveBigIntegerField()
    type = models.CharField(max_length=genericMaxLength)
    speed = models.PositiveIntegerField()


class Cooler(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength) # e.g. Cooler Master
    name = models.CharField(max_length=genericMaxLength) 
    supportedSockets = ArrayField(models.CharField(max_length=genericMaxLength))
    isLiquid = models.BooleanField()
    height = models.PositiveIntegerField() # in mm
    width = models.PositiveIntegerField() # only for water coolers

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'height', 'width'], name='unique_cooler_name_height_width') # some coolers have the same 
            # model name for different variants e.g. 'Aqua Elite V3' for the 120, 240, and 360 mm versions
        ]
    def __str__(self):
        return self.name

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
        return self.CoolerId.name


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
        return self.name


class PSUPrice(models.Model):
    PSUId = models.ForeignKey(PSU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    def __str__(self):
        return str(self.PSUId.wattage)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['PSUId', 'country'], name='unique_psu_country_price')
        ]


class Storage(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength)
    size = models.PositiveIntegerField() # in GB
    isSSD = models.BooleanField()
    formFactor = models.CharField(max_length=genericMaxLength) # e.g. M.2, 2.5, 3.5
    cacheSize = models.PositiveIntegerField() # in MB (Note: might be None)
    isNVMe = models.BooleanField() # for SSDs

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'size'], name='unique_storage_name_size')
        ]
    def __str__(self):
        return self.name + ' ' + str(self.size) + ' GB'


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
        return self.StorageId.name + ' ' + str(self.StorageId.size) + 'GB'
    
class Case(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    name = models.CharField(max_length=genericMaxLength, unique=True)
    formFactor = models.CharField(max_length=genericMaxLength) # e.g. ATX Mid Tower
    moboFormFactors = ArrayField(models.CharField(max_length=genericMaxLength))
    maxGPULength = models.PositiveIntegerField()
    expansionSlots = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    depth = models.PositiveIntegerField()
    threePointFiveDriveBays = models.PositiveIntegerField()
    twoPointFiveDriveBays = models.PositiveIntegerField()
