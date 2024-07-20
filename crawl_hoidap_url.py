from utils import custom_load_page
from collections import defaultdict
import os
import time
import pandas as pd 
import logging
logger = logging.getLogger(__name__)


class QnA_object:
    def __init__(self):
        self.question = []
        self.reference = []
        self.answer = []
    

    # cast to dict
    def to_dict(self):
        return {
            "question": self.question,
            "reference": self.reference,
            "answer": self.answer
        }


def crawl_hoidap(url):
    contents = []
    sub_header = []
    qa = []

    response, soup = custom_load_page(url)
    article = soup.find_all("article")[0]
    header = article.find("header").text.strip()
    
    qa = QnA_object()
    for section in article.find("section", id="news-content"):
        # parse sub header + ignore the muc-luc section
        if (not section.text.strip()) or (section.get("class") == ["accordion", "muc-luc"]):
            continue
        if section.name == "strong":
            sub_header.append(section.text.strip())

        # parse question, reference, answer
        if section.name == "h2": # question block
            if qa.question:
                contents.append(qa.to_dict())
                qa = QnA_object()
            qa.question.append(section.text.strip())
        else:
            if section.name == "p":
                qa.answer.append(section.text.strip())
            elif section.name == "blockquote":
                qa.reference.append(section.text.strip())
    if qa.question:
        contents.append(qa.to_dict())
    return {
        "header": header,
        "sub_header": sub_header,
        "contents": contents
    }
    
NUM_RETRY = 3
if __name__ == "__main__":

    list_url_file = "all_url_tu_van.txt"
    qna_data_file = "qna_data.csv"


    while NUM_RETRY > 0:
        if not os.path.exists(list_url_file):
            logger.warn(f"File {list_url_file} not found")
            NUM_RETRY -= 1
            time.sleep(10) 
        else:
            list_url = open(list_url_file, "r").read().split("\n")
            write_every = 10
            
            df = pd.DataFrame(columns=["url", "header", "sub_header", "contents"])
            if os.path.exists(qna_data_file):
                df = pd.read_csv(qna_data_file)
            
            is_done = True
            for url in list_url:
                if url in df["url"].values:
                    continue
                is_done = False
                data = crawl_hoidap(url)
                df = df._append({
                    "url": url,
                    "header": data["header"],
                    "sub_header": data["sub_header"],
                    "contents": data["contents"]
                }, ignore_index=True)
                if len(df) % write_every == 0:
                    df.to_csv(qna_data_file, index=False)
                logger.info(f"Done {url}")
            df.to_csv(qna_data_file, index=False)
            if is_done:
                break
    
    logger.info("crawl process done")