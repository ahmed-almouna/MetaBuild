from rest_framework import serializers
from .models import *



class CPUSerializer(serializers.ModelSerializer):
    #    name = serializers.CharField(source='cpu_name')


    class Meta:
        model = CPU
        fields = '__all__'
