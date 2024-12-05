from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'travelog'

urlpatterns = [
    path('', views.travel_log, name='travelog'),
    path('get_data_photo/', views.get_data_photo, name='get_data_photo'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)