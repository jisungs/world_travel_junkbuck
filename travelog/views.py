
from django.http import HttpResponse
from django.shortcuts import render

import os
import folium

import base64
from folium import IFrame

# Create your views here.
def travel_log(request):

    #folium

     #Add Marker
    encoded = base64.b64encode(open('media/부산도심.jpg', 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=100, height=100)
    popup = folium.Popup(iframe, max_width=400)

    geocode = [33.3786,126.5662]
    m = folium.Map(location=[33.3786,126.5662], zoom_start=10)

    seogwipo = [33.2532,126.5610]
    
    #  #지도에 마커추가
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