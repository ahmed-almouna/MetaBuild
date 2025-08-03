from rest_framework import serializers
from .models import *


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


