import json
import urllib.request, urllib.parse, urllib.error
import re

data = open('img_links.json')
img_links = json.load(data)


for img in img_links:
    r = urllib.request.urlopen(img)
    if r.status == 200:
        urllib.request.urlretrieve(img, './images/' + re.findall('\/s\/([\S]+)$',img)[0])
