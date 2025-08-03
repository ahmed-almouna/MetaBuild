from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from builder import views

urlpatterns = [
    path("build/", views.getBuild),
    path("addCPU/", views.addCPU.as_view()),
    path("addGPU/", views.addGPU.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)