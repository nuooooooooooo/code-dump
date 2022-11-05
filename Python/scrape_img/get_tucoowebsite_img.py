from cgitb import html
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import json

def getdata(url):
    r = urllib.request.urlopen(url)
    return r

data = open('data.json')

website_links = json.load(data)

lst = list()
for link in website_links:
    html_data = getdata(link)
    soup = BeautifulSoup(html_data,'html.parser')
    for img in soup.find_all('img',attrs= {"width": "88"}):
        img_link = img.get('src', None)
        img_full_link = re.findall('([\S]+)index[0-9]*.htm',link)[0] + img_link
        lst.append(img_full_link)

a_file = open("img_links.json", "w")
json.dump(lst, a_file)
a_file.close()

print(lst)
  