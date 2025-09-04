from rest_framework import serializers
from . import models

# This file contains the serializers for the models.

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CPU
        fields = '__all__'

class CPUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CPUPrice
        fields = '__all__'

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPU
        fields = '__all__'

class GPUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUPrice
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Storage
        fields = '__all__'

class StoragePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoragePrice
        fields = '__all__'

class PSUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PSU
        fields = '__all__'

class PSUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PSUPrice
        fields = '__all__'

class CoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cooler
        fields = '__all__'

class CoolerPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoolerPrice
        fields = '__all__'

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RAM
        fields = '__all__'

class RAMPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RAMPrice
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Case
        fields = '__all__'

class CasePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CasePrice
        fields = '__all__'
