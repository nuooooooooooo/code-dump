import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import re
import json

# based on https://python.plainenglish.io/scraping-the-subpages-on-a-website-ea2d4e3db113
# and https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948


def getdata(url):
    r = urllib.request.urlopen(url)
    return r


dict_href_links = dict()


def get_links(website_link, regex, criteria):

    print('current page link:', website_link)

    html_data = getdata(website_link)
    soup = BeautifulSoup(html_data, "html.parser")

    list_links = list()

    for link in soup.find_all('a', criteria):

        if str(link['href']).startswith('/'):
            link_to_add = link['href'][1:]
        else:
            link_to_add = link['href']

        dict_href_links[link_to_add] = None
        link_with_www = re.findall(regex, str(website_link))[0] + link_to_add
        print("adjusted link =", link_with_www)
        
        if link_with_www not in dict_href_links:
            list_links.append(link_with_www)

    dict_links = dict.fromkeys(list_links, "Not-checked")

    return dict_links


def get_subpage_links(l, criteria, regex="\S+"):
    for link in l:
        if l[link] == "Not-checked":  # if not crawled, start crawling and get links

            dict_link_subpages = get_links(link, regex, criteria)
            l[link] = "Checked"
        else:  # create empty dictionary in case every link is checked
            dict_link_subpages = {}

        l = {**dict_link_subpages, **l}

    return l


website = "http://www.tucoo.com/pixel/index22.htm"
dict_links = {website: "Not-checked"}


counter, counter2 = None, 0

while counter != 0:
    counter2 += 1
    if counter2 == 1:
        dict_links2 = get_subpage_links(
            dict_links, {'id': 'pics'}, '([\S]+)pixel')
    else:
        dict_links2 = get_subpage_links(
            dict_links, {'class': 'navigationtext'}, '([\S]+)index[0-9]*.htm$')

    counter = sum(value == "Not-checked" for value in dict_links2.values())

    print('')
    print('this is loop iteration number ', counter2)
    print("LENGTH OF DICTIONARY WITH LINKS =", len(dict_links2))
    print("NUMBER OF 'Not-checked' LINKS = ", counter)
    print("")
    dict_links = dict_links2

a_file = open("data.json", "w")
json.dump(dict_links, a_file)
a_file.close()

print(dict_href_links)
