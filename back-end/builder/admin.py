from django.contrib import admin
from .models import *

# Admin registered models.

admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Mobo)
admin.site.register(RAM)
admin.site.register(Cooler)
admin.site.register(PSU)
admin.site.register(Case)
admin.site.register(Storage)
admin.site.register(CPUPrice)
admin.site.register(GPUPrice)
admin.site.register(StoragePrice)
admin.site.register(PSUPrice)
admin.site.register(CoolerPrice)


