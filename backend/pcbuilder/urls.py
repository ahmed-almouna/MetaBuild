from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# This file contains the app's URLs.

urlpatterns = [
    path("build/", views.getBuild),          # get a PC build
    path("addcpu/", views.AddCPU.as_view()), # add a CPU to the db
    path("addgpu/", views.AddGPU.as_view()),
    path("addstorage/", views.AddStorage.as_view()),
    path("addpsu/", views.AddPSU.as_view()),
    path("addcooler/", views.AddCooler.as_view()),
    path("addram/", views.AddRAM.as_view()),
    path("addcase/", views.AddCase.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns) # allows the API to be accessed with different extensions e.g. 
    # metabuild.com/build.json, metabuild.com/build.api, etc.