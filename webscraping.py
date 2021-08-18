import os
from os import path, write
from typing_extensions import runtime

from requests.models import Response
import config
from datetime import date
import csv
import requests 
from bs4.element import ResultSet, Tag
from bs4 import BeautifulSoup
import re


def get_page(url: str, headers: dict=None) -> BeautifulSoup:
    url = url
    headers = headers
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    
    return soup

def download_csv(url: str, path: str, fname:str, headers: dict=None):
    try:
        csv_path = os.path.join(path, fname)
        print(f"csv_path?: {csv_path}")
        res = requests.get(url, headers=headers)
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for line in res.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))
    except IOError as error:
        print(f"Error 2. {error}")
        exit
        
        
        
# extracting the most actively managed ETF list, urls by ARK
ark_url = config.ETF_URL
headers = config.ETF_HEADER
ark_home = get_page(ark_url, headers=headers)
rows = ark_home.find_all('tr', class_="", )


for row in rows:
    tds = row.find_all('td')
    symbol = (tds[0].get_text()).rstrip()
    link = (row.find('a', href=True))['href']
    wd = os.path.abspath(os.getcwd())
    parent_path = os.path.join(wd, "data\\etfs")
    path = os.path.join(parent_path, str(date.today()))
    print(f"path: {path}")
    print(os.path.exists(path))
    src = get_page(link, headers=headers)
    regex = re.compile('csv')
    csv_url = (src.find('a', {"id": regex}))['href']
    fname = symbol+'.csv'
    # download_csv(path)
    try:
        os.makedirs(path, mode=755)
        print("Folder Created: "+ path)
    except OSError as error:
        print(f"Folder Cannot be Created {error}")
    
    try:
        download_csv(csv_url, path, fname, headers=headers)
    except IOError as error:
        print(f"File Cannot be Created {error}")
        
        

        

        
    
   
        
        
    
        
    
