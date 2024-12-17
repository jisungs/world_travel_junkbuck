
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import PhotoForm, TravelForm
from .models import PhotoMetadata, Photo

import os
import folium

import base64
from folium import IFrame

from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS




def get_data_photo(request):
    image_file = "media/IMG_4751.JPG"
    image = Image.open(image_file)
    
    exif = {}
    if image._getexif() is not None:
        for tag, value in image._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value

    if "GPSInfo" in exif:
        gps_info=exif["GPSInfo"]

        def convert_to_degrees(value):
            """
            Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format.
            Args:
            value (tuple): The GPS coordinate as a tuple (degrees, minutes, seconds)
            Returns:
            float: The coordinate in degrees
            """
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m/60.0) + (s/3600.0)
        # Convert latitude and longitude to degrees
        lat = convert_to_degrees(gps_info[2])
        lon = convert_to_degrees(gps_info[4])
        lat_ref = gps_info[1]
        lon_ref = gps_info[3]

        # Adjust the sign of the coordinates based on the reference (N/S, E/W)
        if lat_ref != "N":
            lat = -lat
        if lon_ref != "E":
            lon = -lon
        # Format the GPS coordinates into a human-readable string
        geo_coordinate = "{0}° {1}, {2}° {3}".format(lat, lat_ref, lon, lon_ref)
    return geo_coordinate

def get_gps_info(image_path):
    """Extract GPS metadata from an image file."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()  # Extract EXIF data
        if not exif_data:
            return None
        
        gps_info = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_info[sub_decoded] = value[gps_tag]
        
        # GPS 정보가 없으면 None 반환
        if not gps_info:
            return None

        # GPS 데이터를 변환
        def convert_to_degrees(value):
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        
        latitude = convert_to_degrees(gps_info.get("GPSLatitude", (0, 0, 0)))
        longitude = convert_to_degrees(gps_info.get("GPSLongitude", (0, 0, 0)))
        
        # 북/남위, 동/서경 처리
        if gps_info.get("GPSLatitudeRef") == "S":
            latitude = -latitude
        if gps_info.get("GPSLongitudeRef") == "W":
            longitude = -longitude
        
        return {"latitude": latitude, "longitude": longitude}
    
    except Exception as e:
        print(f"Error reading GPS info: {e}")
        return None

def process_all_images(media_root):
    """Process all images in MEDIA_ROOT and extract GPS data."""
    images_with_gps = []
    for root, dirs, files in os.walk(media_root):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png','.JPG')):
                image_path = os.path.join(root, file)
                gps_info = get_gps_info(image_path)
                if gps_info:
                    images_with_gps.append({
                        "file": image_path,
                        "gps": gps_info,
                    })
    return images_with_gps


def photo_image_upload(request):
    form = TravelForm()
    if request.method == 'POST':
        form= TravelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('travelog:main')
        else:
            form=TravelForm()
        return render(request, 'travelog/photo_upload.html', {'form':form})
    return render(request, 'travelog/photo_upload.html', {'form':form})
    



# Create your views here.
def travel_log(request):
    media_root = settings.MEDIA_ROOT    
    gps_datas = process_all_images(media_root)
    #folium
    #Add Marker
    # media/IMG_4751.JPG
    encoded = base64.b64encode(open('media/부산도심.JPG', 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=150, height=150)
    popup = folium.Popup(iframe, max_width=300)

    geocode = [33.3786,126.5662]
    m = folium.Map(location=[33.3786,126.5662], zoom_start=6)
    
    #지도에 마커추가
    folium.Marker(
        location= geocode,
        tooltip= html,
        popup = popup, 
        icon = folium.Icon(color='blue')
    ).add_to(m)

    for item in gps_datas:

        path = item['file'].replace('/Users/jisungs/Documents/dev/sideprojects/world_travel/', '')
        thumnail_path = path.replace('images', 'thumnail').replace('.JPG', '.thumb.JPG')

        encoded = base64.b64encode(open(f"{thumnail_path}", 'rb').read())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=150, height=150)
        popup = folium.Popup(iframe, max_width=300)
        
        geocode = [item['gps']['latitude'],item['gps']['longitude']]

        folium.Marker(
        location=geocode,
        tooltip= html,
        popup=popup,
        icon = folium.Icon(color='blue')
        ).add_to(m)

    # exporting
    map_html=m._repr_html_()
    context = {
        'map_html': map_html,
       
        }
    # rendering
    return render(request, 'travelog/index.html', context)