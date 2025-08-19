import pandas as pd
import folium

# map = folium.Map(location=[36.578, 136.648])

# facilities = pd.read_csv("facilities.csv")
# for latitude, longitude, name_jp in zip(facilities["latitude"], facilities["longitude"], facilities["name_jp"]):
#     folium.Marker([latitude, longitude], popup=name_jp).add_to(map)

stacks = pd.read_csv("stacks.csv")

# map.save("map.html")
