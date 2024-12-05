
from django.http import HttpResponse
from django.shortcuts import render

import os
import folium

import base64
from folium import IFrame

from PIL import Image
from PIL.ExifTags import TAGS


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



# Create your views here.
def travel_log(request):
    #folium

     #Add Marker
    encoded = base64.b64encode(open('media/부산도심.jpg', 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=150, height=150)
    popup = folium.Popup(iframe, max_width=300)

    geocode = [33.3786,126.5662]
    m = folium.Map(location=[33.3786,126.5662], zoom_start=10)

    seogwipo = [33.2532,126.5610]
    
    #지도에 마커추가
    folium.Marker(
        location=geocode,
        tooltip= html,
        popup = popup, 
        icon = folium.Icon(color='blue')
    ).add_to(m)


    folium.Marker(
        location=seogwipo,
        tooltip= html,
        popup=f'서귀포시',
        icon = folium.Icon(color='blue')
    ).add_to(m)

    
    # exporting
    map_html=m._repr_html_()
    context = {'map_html': map_html}

    # rendering

    return render(request, 'travelog/index.html', context)