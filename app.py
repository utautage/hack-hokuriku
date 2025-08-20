import pandas as pd
import folium

map = folium.Map(location=[36.578, 136.648], zoom_start=13)

facilities = pd.read_csv("facilities.csv")
for lat, lng, name_jp in zip(facilities["lat"], facilities["lng"], facilities["name_jp"]):
    folium.Marker([lat, lng], popup=name_jp).add_to(map)

stacks = pd.read_csv("stacks.csv")
routes_dict = {}
for uid, group in stacks.groupby("uid"):
    sorted_group = group.sort_values("datetime")
    routes_dict[uid] = sorted_group[["datetime", "lat", "lng"]].values.tolist()
index = 0
for uid in stacks["uid"].unique():
    route = routes_dict[uid]
    coords = [(r[1], r[2]) for r in route]
    folium.PolyLine(coords, color="blue", weight=3).add_to(map)
    index += 1
    if index>=5:
        break

map.save("map.html")
