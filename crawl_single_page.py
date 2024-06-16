import requests
from bs4 import BeautifulSoup
import random, time
import os


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('crawler.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def custom_load_page(url):
    time.sleep(random.randint(1, 3))
    print(f"Requesting {url}")
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        soup = None
        print(f"Error parsing {url}: {e}")
        logger.error(f"Error parsing {url}: {e}")
        open("error.txt", "a+").write(f"{url}\n {e}\n")
    return response, soup

def do_get_metatadata(soup):
    divThuocTinh = soup.find("div", id="divThuocTinh")
    table_thuoctinh = divThuocTinh.find_all("table")
    if len(table_thuoctinh) == 0:
        return {}
    metadata = {}
    new_key = None
    for td in table_thuoctinh[0].find_all("td"):
        if new_key is None:
            new_key = td.text.strip()
        else:
            metadata[new_key] = td.text.strip()
            new_key = None
    return metadata

def get_metadata(soup):
    try:
        metadata = do_get_metatadata(soup)
        logger.info(f"Get metadata successfully {metadata}")
    except Exception as e:
        metadata = {}
        logger.error(f"Error get metadata: {e}")
    return metadata


def get_keyword(soup):
    keyword = []
    try:
        keyword_div = soup.find("div", class_="tukhoa")
        keyword = [link.text for link in keyword_div.find_all("a")]
        logger.info(f"Get keyword successfully {keyword}")
    except Exception as e:
        logger.error(f"Error get keyword: {e}")
    return keyword

def get_incremental_filename(log_folder, base_filename, extension):
    
    files = os.listdir(log_folder)
    
    # Filter files that match the base filename and extension pattern
    matching_files = [f for f in files if f.startswith(base_filename) and f.endswith(extension)]
    
    # Extract the numeric part from the filenames and find the highest number
    max_num = 0
    for f in matching_files:
        try:
            num = int(f[len(base_filename):-len(extension)])
            if num > max_num:
                max_num = num
        except ValueError:
            continue
    
    # Increment the highest number by 1
    new_num = max_num + 1
    
    # Return the new filename
    new_filename = f"{base_filename}{new_num}{extension}"
    return new_filename


def do_get_content(soup):
    content1 = soup.find("div", class_="content1")
    title = soup.title.text.strip()
    file_name = get_incremental_filename("contents","content_" , ".txt")
    with open(f"contents/{file_name}", "w+") as f:
        f.write(content1.text.strip())    
    return file_name

def get_content(soup):
    try:
        content = do_get_content(soup)
        logger.info(f"Get content successfully {content}")
    except Exception as e:
        content = None
        logger.error(f"Error get content: {e}")
    return content

def crawl_contents(url):
    logger.info(f"Start crawling {url}")
    response, soup = custom_load_page(url)
    metadata = get_metadata(soup)
    content = get_content(soup)
    keyword = get_keyword(soup)    
    return {"url": url, "metadata": metadata, "content": content, "keyword": keyword, "title": soup.title.text.strip()}
