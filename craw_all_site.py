import os
import pandas as pd
import glob
from crawl_single_page import crawl_contents
from bs4 import BeautifulSoup

all_sitemap = glob.glob("sitemap/*.xml")
for i,sitemap in enumerate(all_sitemap):
    lines = []
    xml_string = open(sitemap, "r").read()
    soup = BeautifulSoup(xml_string, "lxml")
    for loc in soup.find_all("loc"):
        url = loc.text
        raw_data = crawl_contents(url)
        lines.append(raw_data)
    if os.path.exists("raw_data.csv"):
        df = pd.read_csv("raw_data.csv")
        df = pd.concat([df, pd.DataFrame(lines)])
        df.to_csv("raw_data.csv", index=False)
    else:
        pd.DataFrame(lines).to_csv("raw_data.csv", index=False)

