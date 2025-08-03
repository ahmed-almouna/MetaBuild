import socket
from django.db import models
from django.contrib.postgres.fields import ArrayField

genericMaxLength = 100
longMaxLength = 500 # for generic string that might be bigger that 100 charachters long e.g. links

# Create your models here.
class CPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True)
    model = models.CharField(max_length=genericMaxLength, unique=True)
    brand = models.CharField(max_length=genericMaxLength)
    series = models.CharField(max_length=genericMaxLength)
    generation = models.PositiveIntegerField()
    socket = models.CharField(max_length=genericMaxLength)
    architecture = models.CharField(max_length=genericMaxLength)
    coreCount = models.PositiveIntegerField() # effeciency + performance cores
    threadCount = models.PositiveIntegerField()
    boostClock = models.PositiveIntegerField()
    TDP = models.PositiveIntegerField()
    cacheSize = models.PositiveIntegerField() # L2 + L3
    coolerIncluded = models.BooleanField()
    integratedGPU = models.CharField(max_length=genericMaxLength) # can be None or specific model
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.model

class CPUPrice(models.Model):
    CPUId = models.ForeignKey(CPU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    available = models.BooleanField()
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength, null=True, blank=True)

    def __str__(self):
        return self.CPUId.model

class GPU(models.Model):
    pcPartPickerId = models.CharField(max_length=genericMaxLength, unique=True, default="car")
    model = models.CharField(max_length=genericMaxLength, unique=True) # e.g. RTX 3060
    brand = models.CharField(max_length=genericMaxLength) # e.g. nvidia, amd
    manufacturer = models.CharField(max_length=genericMaxLength) # e.g. gigabyte, asus
    series = models.CharField(max_length=genericMaxLength) # e.g. 5000, 7000 *note this is like generation to CPU
    name = models.CharField(max_length=genericMaxLength) # e.g. Ventus 2X
    boostClock = models.PositiveIntegerField()
    VRAM = models.PositiveIntegerField()
    TDP = models.PositiveIntegerField()

    def __str__(self):
        return self.model

class GPUPrice(models.Model):
    GPUId = models.ForeignKey(GPU, on_delete=models.CASCADE)
    country = models.CharField(max_length=genericMaxLength)
    available = models.BooleanField()
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength, null=True, blank=True)

    def __str__(self):
        return self.GPUId.model

class Mobo(models.Model):
    name = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    socket = models.CharField(max_length=genericMaxLength)
    formFactor = models.CharField(max_length=genericMaxLength)
    chipset = models.CharField(max_length=genericMaxLength)
    memoryType = models.CharField(max_length=genericMaxLength)
    memorySlots = models.PositiveIntegerField()
    memorySpeed = models.PositiveIntegerField() # max memory speed supported
    mDotTwoSlots = models.PositiveIntegerField()
    sataSlots = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)
    
class RAM(models.Model):
    name = models.CharField(max_length=genericMaxLength)
    manufacturer = models.CharField(max_length=genericMaxLength)
    type = models.CharField(max_length=genericMaxLength)
    speed = models.PositiveIntegerField()
    amount = models.PositiveBigIntegerField()
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)


class Cooler(models.Model):
    name = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    supportedSockets = ArrayField(models.CharField(max_length=genericMaxLength))
    isLiquid = models.BooleanField()
    size = models.PositiveIntegerField(null=True) # e.g. 360mm (only for water)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)


class PSU(models.Model):
    name = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    formFactor = models.CharField(max_length=genericMaxLength)
    isModular = models.BooleanField()
    wattage = models.PositiveIntegerField()
    efficiency = models.CharField(max_length=genericMaxLength)
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)


class Case(models.Model):
    name = models.CharField(max_length=genericMaxLength, unique=True)
    manufacturer = models.CharField(max_length=genericMaxLength)
    formFactor = models.CharField(max_length=genericMaxLength)
    moboFormFactors = ArrayField(models.CharField(max_length=genericMaxLength))
    price = models.PositiveIntegerField()
    buyLink = models.URLField(max_length=longMaxLength)

    