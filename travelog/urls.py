from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'travelog'

urlpatterns = [
    path('', views.travel_log, name='travelog'),
    path('test/', views.test, name ='test'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)