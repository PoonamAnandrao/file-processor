from django.contrib import admin
from django.urls import path
from .views import FileProcessorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'file', FileProcessorViewSet, basename='file')

urlpatterns = [
]

urlpatterns += router.urls