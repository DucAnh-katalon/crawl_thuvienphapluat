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
    logger.info(f"Requesting {url}")
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        soup = None
        logger.error(f"Error parsing {url}: {e}")
        open("error.txt", "a+").write(f"{url}\n {e}\n")
    return response, soup