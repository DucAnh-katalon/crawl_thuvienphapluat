from bs4 import BeautifulSoup
import requests
from utils import custom_load_page
import logging
logger = logging.getLogger(__name__)
import os

if __name__ == "__main__":
    
    all_url_tu_van_url_file = "all_url_tu_van.txt"
    if os.path.exists(all_url_tu_van_url_file):
        all_url_tu_van_url = open(all_url_tu_van_url_file).read().split("\n")
    else:
        all_url_tu_van_url = []


    phapluat_site = "https://thuvienphapluat.vn/phap-luat/"
    phapluat_soup = BeautifulSoup(requests.get(phapluat_site).text, "html.parser")
    categorical_phapluat_link = [phapluat_site + link.get("href") for link in  phapluat_soup.find("div", class_="newsfieldsbottom").find_all("a")]

    logger.info(f"Number of categorical link: {len(categorical_phapluat_link)}")
    logger.info(f"List of categorical link: {categorical_phapluat_link}")
    
    for categorical_link in categorical_phapluat_link:
        logger.info(f"Processing {categorical_link}")
        page = 1
        while True:
            flag = False
            url_with_page = categorical_link + f"?page={page}"
            logger.info(url_with_page, "number of url", len(all_url_tu_van_url))
            _, categorical_soup = custom_load_page(url_with_page)
            list_all_queries = [ "https://thuvienphapluat.vn" +  _.find("a").get("href") for _ in categorical_soup.find_all("article") if _.find("a")]
            for url in list_all_queries:
                if url not in all_url_tu_van_url:
                    flag = True
                    all_url_tu_van_url.append(url)
            if not flag:
                break
            page += 1
            open(all_url_tu_van_url_file, "w+").write("\n".join(all_url_tu_van_url))