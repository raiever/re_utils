import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import pandas as pd

import re_utils
import mysql.connector
from config import MYSQL
from date import today

def make_url(index_no):
    url_1 = """\
https://www.rightmove.co.uk/property-for-sale/find.html?\
locationIdentifier=REGION%5E972\
&maxPrice=1000000\
&radius=5.0"""
    index = '&index=%d' % index_no
    url_2 = """\
&propertyTypes=detached%2Csemi-detached%2Cterraced\
&primaryDisplayPropertyType=houses\
&includeSSTC=true"""
    full_url = url_1 + index + url_2
    return full_url

def make_url_list(test=1, index_no=0, url_list=[]):
    while True:
        full_url = make_url(index_no)
        r = requests.get(full_url)
        if r.status_code == 200:
            # print(full_url, ':', r.status_code, '/n')
            url_list.append(full_url)
            index_no += 24  # 0, 24, 48, 72, 96, ...
        else:
            print(full_url, ':', r.status_code)
            break
        if test == 1 and index_no == 120:
            break
    return url_list

def get_property_id(url):
    id_list_per_url = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    p = re.compile(r'[\d]+')
    for a in soup.select("div.propertyCard-details a.propertyCard-link"):
        property_id = (p.search(str(a.get('href')))).group() # property ID 
        # print(a.get('href')) # link: /property-for-sale/property-75515954.html
        id_list_per_url.append(int(property_id))
    return id_list_per_url

def get_id_list(url_list):
    id_list_total = []
    for url in url_list:
        id_list_per_url = get_property_id(url)
        print('Length of id list: ', len(id_list_per_url))
        id_list_total += id_list_per_url
    return id_list_total

def get_title(specific_link):
    try:
        r = requests.get(specific_link)
    except Exception as e:
        print(e, ':', specific_link)
    soup = BeautifulSoup(r.content, 'lxml')
    print('title:', soup.select('div.left h1')[0].text)
    try:
        title = soup.select('div.left h1')[0].text
    except:
        title = 'None'
    return title

def get_address(specific_link):
    try:
        r = requests.get(specific_link)
    except Exception as e:
        print(e, ':', specific_link)
    soup = BeautifulSoup(r.content, 'lxml')
    print('address:', soup.select('div.left meta[itemprop="streetAddress"]')[0])
    try:
        address = re_utils.get_content_value(soup.select('div.left meta[itemprop="streetAddress"]')[0])
    except:
        address = 'None'
    return address

def get_price(specific_link):
    p = re.compile(r'[\£\,]')
    try:
        r = requests.get(specific_link)
    except Exception as e:
        print(e, ':', specific_link)
    soup = BeautifulSoup(r.content, 'lxml')
    print('price:', int(p.sub('', soup.select('div.property-header-bedroom-and-price p#propertyHeaderPrice strong')[0].text.strip())))
    try:
        temp = soup.select('div.property-header-bedroom-and-price p#propertyHeaderPrice strong')[0].text.strip()
        price = int(p.sub('', temp))
    except:
        price = None
    return price


if __name__ == '__main__':
    url = make_url(index_no=0)
    print(url)
    url_list = make_url_list(test=1, index_no=0, url_list=[])
    id_list_total = get_id_list(url_list)
    print('Length of id_list_total: ', len(set(id_list_total)))

    cnx = mysql.connector.connect(**MYSQL)
    cursor = cnx.cursor()

    query_1 = ("INSERT INTO property_list "
               "(property_id, title, address, price) "
               "VALUES (%s, %s, %s, %s)")

    today = today()
    query_2 = ("ALTER TABLE property_list "
               "ADD %s_price INT(11);" % today)
    cursor.execute(query_2)
    
    # Initial DB
    for property_id in set(id_list_total):
        specific_link = "https://www.rightmove.co.uk/property-for-sale/property-%d.html" % property_id
        print(specific_link)
        title = get_title(specific_link)
        address = get_address(specific_link)
        price = get_price(specific_link)
        data = (property_id, title, address, price)
        cursor.execute(query_1, data)
        print()
    
    cnx.commit()
    cursor.close()
    cnx.close()
