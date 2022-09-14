from pickle import TRUE
from tkinter.ttk import Style
import folium
import pandas as pd
data = pd.read_csv("volcano.csv")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
elev = list(data["Elev"])
name = list(data["Volcano Name"])


def color_producer(elevation):
    if (elevation < 1000):
        return 'green'
    elif (1000 <= elevation < 3000):
        return 'orange'
    else:
        return 'red'


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
map = folium.Map(location=[34.5, 131.6], zoom_start=6, tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=folium.Popup(
        iframe), color='black', fill_color=color_producer(el), fill=TRUE, fill_opacity=1))

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 10000000
                                                       else 'orange' if 10000000 <= x['properties']['POP2005'] <= 20000000 else 'red'}))
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
