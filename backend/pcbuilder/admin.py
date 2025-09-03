from django.contrib import admin
from . import models

# Admin registered models.

admin.site.register(models.CPU)
admin.site.register(models.GPU)
admin.site.register(models.Mobo)
admin.site.register(models.RAM)
admin.site.register(models.Cooler)
admin.site.register(models.PSU)
admin.site.register(models.Case)
admin.site.register(models.Storage)
admin.site.register(models.CPUPrice)
admin.site.register(models.GPUPrice)
admin.site.register(models.StoragePrice)
admin.site.register(models.PSUPrice)
admin.site.register(models.CoolerPrice)
admin.site.register(models.RAMPrice)
admin.site.register(models.CasePrice)
