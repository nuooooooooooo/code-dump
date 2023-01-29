from math import radians, cos, sin, asin, sqrt
import json

# haversine from https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


f = open('poi.json')
f2 = open('panelsSF.json')
f3 = open('panelsBB.json')


POI = json.load(f)
SF = json.load(f2)
BB = json.load(f3)


def is_in_dist_of_POI(POI, panels, radius,d):
    for poi_loc, poi_coords in POI.items():
        for panel_loc, panel_coords in panels.items():
            dist = haversine(poi_coords['Longitude'], poi_coords['Latitude'], panel_coords['Longitude'], panel_coords['Latitude'])
            if poi_loc not in d:
                d[poi_loc] = {}
            if dist <= radius:
                d[poi_loc][f'within_{radius}km'] = d[poi_loc].get(f'within_{radius}km',0)+1
    return d

def panel_in_dist_of_POI(POI, panels, radius,d):
  for panel_ref, panel_coords in panels.items():
    for poi_loc, poi_coords in POI.items():
        dist = haversine(poi_coords['Longitude'], poi_coords['Latitude'], panel_coords['Longitude'], panel_coords['Latitude'])
        if panel_ref not in d:
                d[panel_ref] = {}
        if dist <= radius:
          d[panel_ref][f"Covers POI within {radius} km"] = True
          print(panel_ref)
          break
        else:
          d[panel_ref][f"Covers POI within {radius} km"] = False
  return d

def list_in_dist_of_POI(POI, panels, radius,d):
    for poi_loc, poi_coords in POI.items():
      lst = list()
      for panel_loc, panel_coords in panels.items():
          dist = haversine(poi_coords['Longitude'], poi_coords['Latitude'], panel_coords['Longitude'], panel_coords['Latitude'])
          if poi_loc not in d:
              d[poi_loc] = {}
          if dist <= radius:
              lst.append(panel_loc)
              d[poi_loc][f'within_{radius}km'] = lst
    return d
                

d = dict()
is_within_5km_SF = is_in_dist_of_POI(POI, SF, 5.00,d)
is_within_3km_SF = is_in_dist_of_POI(POI, SF, 3.00,d)

d2 = dict()
is_within_5km_BB = is_in_dist_of_POI(POI, BB, 5.00,d2)
is_within_3km_BB = is_in_dist_of_POI(POI, BB, 3.00,d2)

a_file = open("SFproximity.json", "w")
json.dump(d, a_file)
a_file.close()

b_file = open("BBproximity.json", "w")
json.dump(d2, b_file)
b_file.close()

f.close()
f2.close()
f3.close()

