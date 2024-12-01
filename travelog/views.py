
from django.http import HttpResponse
from django.shortcuts import render

import os
import folium

# Create your views here.
def travel_log(request):
    # return HttpResponse('hello world')
    shp_dir = os.path.join(os.getcwd(),'media','shp')

    #folium
    geocode = [33.3786,126.5662]
    m = folium.Map(location=[33.3786,126.5662], zoom_start=10)
    
     #지도에 마커추가
    folium.Marker(
        location=geocode,
        popup=f'제주도',
        icon = folium.Icon(color='blue')
    ).add_to(m)
    
    # exporting
    map_html=m._repr_html_()
    context = {'map_html': map_html}

    # rendering


    return render(request, 'travelog/index.html', context)