from rest_framework import serializers
from .models import *



class CPUSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CPU
        fields = '__all__'



