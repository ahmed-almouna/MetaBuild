from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pcbuilder_app import views

# Site's URLs.

urlpatterns = [
    path("build/", views.getBuild), # get a PC build
    path("addCPU/", views.addCPU.as_view()),
    path("addGPU/", views.addGPU.as_view()),
    path("addStorage/", views.addStorage.as_view()),
    path("addPSU/", views.addPSU.as_view()),
    path("addCooler/", views.addCooler.as_view()),
    path("addRAM/", views.addRAM.as_view()),
    path("addCase/", views.addCase.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) # allows the API to be accessed with different extensions e.g. 
                                                  # MetaBuild/build.json, MetaBuild/build.api, etc.