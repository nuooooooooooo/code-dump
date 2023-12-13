# pip3 install xlrd==1.2.0
# pip3 install excel2json-3
# pip3 install json2excel

import excel2json
import xlrd
from json2excel import Json2Excel
from math import radians, cos, sin, asin, sqrt
import json
import re
import os
from datetime import datetime

if __name__ == '__main__':
    json2excel = Json2Excel(export_dir="./output/")
    json2excel2 = Json2Excel(export_dir="./output/")



# haversine from https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
def haversine(lon1, lat1, lon2, lat2):
  """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
  if lon1 == "" or lon2 == "" or lat1 == "" or lat2 == "":
      return None

  # convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

  # haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * asin(sqrt(a))
  r = 6371  # Radius of earth in kilometers. Use 3956 for miles
  return c * r

def clean_folder(panels_path,poi_path):
  for file in os.listdir(panels_path):
          if file.endswith('.json'):
              os.remove(panels_path+file)
  for file in os.listdir(poi_path):
          if file.endswith('.json'):
              os.remove(poi_path+file)

userfile = input('Panel List Filename: ')
poifile = input('POI filename: ')
panels_path = "./data/panels_json/"
poi_path = "./data/poi_json/"
distances_path = "./data/distances.csv"

clean_folder(panels_path, poi_path)

filename_without_extension = re.findall('([\s\w\d\-]+).xlsx$', userfile)

excel2json.convert_from_file(filepath=userfile,location=panels_path)
excel2json.convert_from_file(filepath=poifile,location=poi_path)


for file in os.listdir(panels_path):
        if file.endswith('.json'):
            f = open(panels_path + file)
for file in os.listdir(poi_path):
        if file.endswith('.json'):
            f3 = open(poi_path + file)

POI = json.load(f3)
BB = json.load(f)




def is_in_dist_of_POI(POI, panels, radius, d):
  for poi in POI:
    for panel in panels:
        dist = haversine(poi['Longitude'], poi['Latitude'], panel['Longitude'], panel['Latitude'])
        poi_loc = poi["ID"] 
        if poi_loc not in d:
           d[poi_loc] = {}
        
        if dist != None and dist <= radius:
          d[poi_loc][f'within_{radius}km'] = d[poi_loc].get(f'within_{radius}km', 0) + 1
        else:
          d[poi_loc][f'within_{radius}km'] = d[poi_loc].get(f'within_{radius}km', 0) 
  # print(d)
  return d

        

def panel_in_dist_of_POI(POI, panels, radius, d):
   for panel in panels:
     for poi in POI:
       dist = haversine(poi['Longitude'], poi['Latitude'],
                        panel['Longitude'], panel['Latitude'])
       panel_ref = panel["ID"]
       if panel_ref not in d:
         d[panel_ref] = {}
       if dist != None and dist <= radius:
         d[panel_ref][f"Covers POI within {radius} km"] = True
         break
       else:
         d[panel_ref][f"Covers POI within {radius} km"] = False
  #  print(d)
   return d

def format_d_for_excel(d):
  json_format = []
  for id, criteria in d.items():
    temp = dict()
    temp["ID"] = id
    for key in criteria:
      temp[key] = criteria[key]
    json_format.append(temp)   
  return json_format

d = dict()
d2 = dict()
fhand = open(distances_path)
for line in fhand:
  line = float(line.strip())
  panel_within_6km_SF = is_in_dist_of_POI(POI, BB, line, d)
  list_within_6km_BB = panel_in_dist_of_POI(POI, BB, line, d2)


jsons_poi = format_d_for_excel(d)
jsons_panels = format_d_for_excel(d2)
today_date = str(datetime.now().strftime("%Y%m%d"))
json2excel.run(jsons_poi, file_name=f"{filename_without_extension[0]}_poi_analysis_{today_date}.xls")

json2excel2.run(jsons_panels, file_name=f"{filename_without_extension[0]}_panels_analysis_{today_date}.xls")


f.close()
f3.close()
clean_folder(panels_path, poi_path)
