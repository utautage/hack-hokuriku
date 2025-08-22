import pandas as pd
import folium
import colorsys

map = folium.Map(location=[36.578, 136.648], zoom_start=13)

class Facility:
    def __init__(self, area, industry, name, location):
        self.area = area
        self.industry = industry
        self.name = name
        self.location = location # (緯度, 経度)

facility_csv = pd.read_csv("facilities.csv")
facilities = {}
for facility in facility_csv.itertuples():
    facilities[facility.device_id] = Facility(facility.area, facility.industry, facility.name_jp, (facility.lat, facility.lng))

stacks = pd.read_csv("stacks.csv")
visit_count = {}
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
for device_id, data in facilities.items():
    icon = color = None
    match data.industry:
        case "体験・観光施設":
            icon = "camera"
            color = "lightgreen"
        case "重要交通施設":
            icon = "plane"
            color = "lightgray"
        case "特産品・小売店":
            icon = "shopping-cart"
            color = "orange"
        case "その他":
            icon = "info-sign"
            color = "red"
        case "飲食店":
            icon = "cutlery"
            color = "lightblue"
    count = 0
    if device_id in visit_count:
        count = visit_count[device_id]
        folium.Circle(data.location, radius=10000 * count / visit_count_max, fill=True, color=color).add_to(map)
    folium.Marker(data.location, f"{data.name}({count})", icon=folium.Icon(color=color, icon=icon)).add_to(map)

route_count_sorted = list(set(route_count.values()))
route_count_sorted.sort(reverse=True)
for (device_id1, device_id2), count in route_count.items():
    rank = route_count_sorted.index(count) / (len(route_count_sorted) - 1)
    weight = 10 - 9 * rank
    r, g, b = colorsys.hsv_to_rgb(0.75 * rank, 0.5, 1)
    folium.PolyLine(
        locations=[facilities[device_id1].location, facilities[device_id2].location],
        weight=weight,
        color=f"#{int(255 * r):02x}{int(255 * g):02x}{int(255 * b):02x}"
    ).add_to(map)

map.save("map.html")
