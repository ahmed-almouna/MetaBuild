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

