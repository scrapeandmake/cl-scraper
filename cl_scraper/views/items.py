from flask import render_template, flash, redirect, Blueprint, url_for
from flask.ext.login import login_required, current_user

from ..models import Item, Image
from ..extensions import db
import http.client
import re
from bs4 import BeautifulSoup


items = Blueprint("items", __name__)


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
    for p in paragraphs:
        if 'Posted' in p.text:
            posted = p.text.replace('Posted: ','')
        return posted


def image_lookup(bsoup_item):
    ind_page = url_request(bsoup_item)
    souped_item = BeautifulSoup(ind_page)
    try:
        img_links = souped_item.find('figure').find_all('img', src=True)
        return [image["src"].split("src=")[-1] for image in img_links]
    except:
        return None

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
    if desc:
        desc = desc.getText().strip()
        return desc[:254]
    else:
        return None

def name_lookup(bsoup_item):
    lookup = bsoup_item.find('h2', attrs={'class' :'postingtitle'})
    if lookup:
        lookup = lookup.text.strip()
        return lookup
    else:
        return None

def item_lookup(bsoup_item):

    ind_page = url_request(bsoup_item)
    souped_item = BeautifulSoup(ind_page)

    name = name_lookup(souped_item)
    url = 'http://raleigh.craigslist.com{}'.format(bsoup_item)
    created = date_lookup(souped_item)
    latitude, longitude = lat_long_lookup(souped_item)
    description = description_lookup(souped_item)

    return {'name':name, 'url':url, 'latitude':latitude, 'created':created,
            'longitude':longitude, 'description':description}

def run_full_lookup():
    souped_page = BeautifulSoup(url_request())
    live_item_list = [item.find('a')['href']
                      for item in souped_page.find_all('p')]

    for item in live_item_list[:25]:
        new_item = Item(**item_lookup(item))
        db.session.add(new_item)
        db.session.commit()
        if image_lookup(item):
            for image in image_lookup(item):
                new_image = Image(item_id=new_item.id, image=image)
                db.session.add(new_image)
    db.session.commit()
