#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
import streamlit as st


# # FETCH A GAME'S TAGS AND POSSIBLE MATCHES

# In[2]:


urgame = input("Enter the link: ")


# In[3]:


# https://store.steampowered.com/app/108600/Project_Zomboid/
# https://store.steampowered.com/app/242760/The_Forest/
# https://store.steampowered.com/app/447530/VA11_HallA_Cyberpunk_Bartender_Action/

#Fetch all the tags
def get_tags(gamelink):
    r = requests.get(gamelink)
    soup = bs(r.content, 'html.parser')
    tags = soup.find("div", attrs={"class": "glance_tags_ctn popular_tags_ctn"}).find_all("a")
    fintags = []
    for oi in tags:
        oi = str(oi)
        taggie = oi.split(">")[1]
        taggie.replace("\t", "")
        fintags.append(taggie[14:-15])
    return fintags

#Fetch all the matches
def num_matches(game1, game2): 
    xo = get_tags(game1)
    yo = get_tags(game2)
    xoi = len((set(xo)) & set(yo))
    yoi = set(xo) & set(yo)
    if xoi > 1:
        print(f'There are {xoi} tags that match.')
        print(f'These tags are: {yoi}')
    elif xoi == 0:
        print(f'There are no tags that match.')
    else:
        print(f'There is {xoi} tag that matches.')
        print(f'This tag is: {yoi}')


# # FETCH SPECIALS

# In[4]:


import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = "https://store.steampowered.com/specials"
path = "C:/AMD/chromedriver.exe"

service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(8)
soups = bs(driver.page_source, 'html.parser')
games = soups.find_all("div", attrs={"class": "ImpressionTrackedElement"})
while games == 0:
    games = soups.find_all("div", attrs={"class": "ImpressionTrackedElement"})
games


# In[5]:


#soups.find_all("div", attrs={"class": "salepreviewwidgets_TitleCtn_1F4bc"})
#soups.find("div", attrs={"class": "ImpressionTrackedElement"}).find("a", attrs={"class": "Focusable"}).get('href')
#soups.find("div", attrs={"class": "ImpressionTrackedElement"}).find("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).get('href')
#soups.find("div", attrs={"class": "ImpressionTrackedElement"}).find("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).find_next("a", attrs={"class": "Focusable"}).get('href')


# In[6]:


finallist = []
y = 0
f = soups.find("div", attrs={"class": "ImpressionTrackedElement"}).find("a", attrs={"class": "Focusable"})
fi = f.get('href')
finallist.insert(0, fi)
while y != 16:
    y += 1
    f = f.find_next("div", attrs={"class": "ImpressionTrackedElement"}).find("a", attrs={"class": "Focusable"})
    fo = f.get('href')
    finallist.append(fo)
finallist


gamername = []
gamermatch = []
gamerdisc = []
pricewas = []
priceis = []
intags = []
oi = 0
for x in finallist:
    nameofthegame = requests.get(x)
    soupi = bs(nameofthegame.content, 'html.parser')
    nick = soupi.find("div", attrs={"class": "apphub_AppName"}).get_text()
    try:
        disc = soupi.find("div", attrs={"class": "discount_pct"}).get_text()
        discprice = soupi.find("div", attrs={"class": "discount_final_price"}).get_text()
        orprice = soupi.find("div", attrs={"class": "discount_original_price"}).get_text()
        oi += 1
        print(f"'{nick}' is sold at a {disc} discount and now costs {discprice} instead of {orprice} Its tags are:")
    except AttributeError:
        print(f"{nick} is not on Steam and/or not sold in Russia - it should be played on a different platform. Its tags are:")
    print(get_tags(x))
    num_matches(urgame, x)
    xoq = get_tags(urgame)
    yoq = get_tags(x)
    yoiq = set(xoq) & set(yoq)
    xoz = len((set(xoq)) & set(yoq))
    gamername.append(nick)
    gamermatch.append(xoz)
    gamerdisc.append(disc)
    pricewas.append(orprice)
    priceis.append(discprice)
    intags.append(yoiq)
    print('')


# In[8]:


df = pd.DataFrame()
df['Game names'] = gamername
df['Price is'] = priceis
df['Price was'] = pricewas
df['Discount percentage'] = gamerdisc
df['Mutual Tags'] = intags
kok = df.duplicated(subset=['Price is'])
f = df[kok].index
dupin = []
for i in f:
    dupin.append(i)
df['Price is'].iloc[dupin] = "Not found"
df['Price was'].iloc[dupin] = "Not found"
df['Discount percentage'].iloc[dupin] = "Not found"
df


# In[9]:


st.title('Steam Recommendations')
st.image('photo.jpg')
st.dataframe(df)


# In[ ]:




