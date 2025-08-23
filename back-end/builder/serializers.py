from rest_framework import serializers
from .models import *

# Serializers.

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'

class CPUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUPrice
        fields = '__all__'

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'

class GPUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPUPrice
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class StoragePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePrice
        fields = '__all__'

class PSUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSU
        fields = '__all__'

class PSUPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSUPrice
        fields = '__all__'

class CoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooler
        fields = '__all__'

class CoolerPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoolerPrice
        fields = '__all__'

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'

class RAMPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMPrice
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class CasePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasePrice
        fields = '__all__'
