import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import time
import random
import string
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
def write(l):
    with open("AllLinks.txt",'a') as f:
        print(l, file=f)
def scrap(val):
    df=pd.read_csv("Product.csv")
    for i in range(31952):
        url="https://www.amazon.in/s?k="
        input = df['title'][i].replace(" ","")
        input = re.sub(r'[^\w\s]', '', input)
        input = input.replace("\xa0", "")
        url = url+input+'&tbm=isch'
        try:
            html = urlopen(Request(url, headers={'User-Agent': generate_random_string(5)}))
            soup = BeautifulSoup(html.read(),'html.parser')
            img_tag = soup.find('img', class_="s-image")
            src_value = img_tag['src']
            link=src_value
        except:
            link="/static/img/Image_not_available.png"
        print(i)
        write(link)
scrap(0)