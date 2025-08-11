from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from builder import views

# URLs.

urlpatterns = [
    path("build/", views.getBuild), # get a PC build
    path("addCPU/", views.addCPU.as_view()),
    path("addGPU/", views.addGPU.as_view()),
    path("addStorage/", views.addStorage.as_view()),
    path("addPSU/", views.addPSU.as_view()),
    path("addCooler/", views.addCooler.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)