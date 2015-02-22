import http.client
import re
from bs4 import BeautifulSoup

def url_request(path='/search/zip/'):

    server = http.client.HTTPConnection('raleigh.craigslist.org')
    server.putrequest('GET', path)
    server.putheader('Accept', 'text/html')
    server.endheaders()
    reply = server.getresponse()

    if reply.status != 200:
        return 'Error sending request {0} {1}'.format(reply.status,
                                                      reply.reason)
    else:
        data = reply.readlines()
        page = ''
        for line in data:
            page += line.decode('utf-8')
        reply.close()
        return page


def date_lookup(bsoup_item):
    paragraphs = bsoup_item.find_all('p', attrs={'class' : 'postinginfo'})
    output_list = []
    for p in paragraphs:
        if 'Posted' in str(p) or 'updated' in str(p):
            output_list.append(p.text)
    return output_list


def image_lookup(bsoup_item):
    try:
        img_links = bsoup_item.find('figure').find_all('img', src=True)
        return [image["src"].split("src=")[-1] for image in img_links]
    except:
        return 'no image'

def lat_long_lookup(bsoup_item):

    location = bsoup_item.find('div', attrs={'class' : 'viewposting'})
    if location:
        item_lat = location["data-latitude"].split("data-latitude=")[-1]
        item_long = location["data-longitude"].split("data-longitude=")[-1]
        return item_lat, item_long
    else:
        return (None, None)

def description_lookup(bsoup_item):
    desc = bsoup_item.find('section', attrs={'id' : 'postingbody'})
    desc = desc.getText().strip()
    if desc:
        return desc
    else:
        return None

def name_lookup(bsoup_item):
    item = bsoup_item.find('h2', attrs={'class' :'postingtitle'}).text.strip()
    if item:
        return item
    else:
        return None

def item_lookup(bsoup_item):

    ind_page = url_request(bsoup_item)
    souped_item = BeautifulSoup(ind_page)

    item_name = name_lookup(souped_item)
    item_url = 'http://raleigh.craigslist.com{}'.format(bsoup_item)
    item_dates = date_lookup(souped_item)
    item_images = image_lookup(souped_item)
    item_lat, item_long = lat_long_lookup(souped_item)
    item_description = description_lookup(souped_item)

    return (item_name, item_url, item_dates, item_images,
            item_lat, item_long, item_description)

def run_full_lookup():

    souped_page = BeautifulSoup(url_request())
    live_item_list = [item.find('a')['href'] for item in souped_page.find_all('p')]

    return [item_lookup(item) for item in live_item_list[:4]]

print(run_full_lookup())
