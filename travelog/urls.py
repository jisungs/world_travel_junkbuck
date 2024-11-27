from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'travelog'

urlpatterns = [
    path('', views.travel_log, name='travelog'),
]