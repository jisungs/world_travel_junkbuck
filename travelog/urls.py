from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'travelog'

urlpatterns = [
    path('', views.travel_log, name='main'),
    path('upload/', views.photo_image_upload, name='photo_upload'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)