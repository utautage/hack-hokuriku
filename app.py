import pandas as pd
import folium

map = folium.Map(location=[36.578, 136.648], zoom_start=13)

class Facility:
    def __init__(self, area, industry, name, location):
        self.area = area
        self.industry = industry
        self.name = name
        self.location = location # (緯度, 経度)

facilities = {}
for facility in pd.read_csv("facilities.csv").itertuples():
    facilities[facility.device_id] = Facility(facility.area, facility.industry, facility.name_jp, (facility.lat, facility.lng))

stacks = pd.read_csv("stacks.csv")
visit_count = {}
# (場所1, (<) 場所2) = 移動回数
route_count = {}
for uid, group in stacks.groupby("uid"):
    sorted_group = group.sort_values("datetime")
    date_memo = ""
    device_id_memo = None
    for datetime, device_id in zip(sorted_group["datetime"], sorted_group["device_id"]):
        # 日付が異なるデータは別の移動とみなす
        if  datetime[0:10] != date_memo:
            device_id_memo = None
        date_memo = datetime[0:10]
        if device_id != device_id_memo:
            if device_id_memo != None:
                route = (device_id, device_id_memo) if device_id < device_id_memo else (device_id_memo, device_id)
                if route not in route_count:
                    route_count[route] = 1
                else:
                    route_count[route] += 1
            device_id_memo = device_id
            if device_id not in visit_count:
                visit_count[device_id] = 1
            else:
                visit_count[device_id] += 1

visit_count_max = max(visit_count.values())
print(visit_count_max)

for device_id, data in facilities.items():
    count = 0
    if device_id in visit_count:
        count = visit_count[device_id]
        folium.Circle(data.location, radius=10000 * count / visit_count_max, fill=True).add_to(map)
    folium.Marker(data.location, f"{data.name}({count})").add_to(map)

route_count_max = max(route_count.values())
print(route_count_max, len(route_count))
for (device_id1, device_id2), count in route_count.items():
    folium.PolyLine([facilities[device_id1].location, facilities[device_id2].location], weight=max(1, 50.0 * count / route_count_max)).add_to(map)

map.save("map.html")
