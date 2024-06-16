import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import random
import time 


def custom_request_and_parse(url):
    time.sleep(random.randint(1, 3))    
    print(f"Requesting {url}")
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, "lxml")
        open(f"sitemap/{url.split('/')[-1]}", "w+").write(response.text)
    except Exception as e:
        soup = None
        print(f"Error parsing {url}: {e}")
        open("error.txt", "a+").write(f"{url}\n {e}\n")
    return response, soup


all_xml_map = []
all_url = []


def traverse_xml(url, all_xml_map, all_url):
    response, soup = custom_request_and_parse(url)
    for loc in soup.find_all("loc"):
        child_url = loc.text
        if ".xml" in child_url:
            if child_url not in all_xml_map:
                all_xml_map.append(url)
                all_xml_map, all_url = traverse_xml(child_url, all_xml_map, all_url)
        else:
            if child_url not in all_url:
                all_url.append(child_url)
    return all_xml_map, all_url

traverse_xml("https://thuvienphapluat.vn/sitemap.xml", all_xml_map, all_url)        
open("sitemap/all_url.txt", "w+").write("\n".join(all_url))
open("sitemap/all_xml_map.txt", "w+").write("\n".join(all_xml_map))