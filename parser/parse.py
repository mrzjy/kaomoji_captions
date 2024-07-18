import os
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from parser.schema import Caption, save_samples

cache_dir = "../.cache"


def load_html(url, filename):
    filepath = os.path.join(cache_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding="utf-8") as f:
            return f.read()
    try:
        r = requests.get(url)
        r.encoding = "utf-8"
        html = r.text
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(html)
        print(filepath, " saved.")
        return html
    except:
        print(traceback.format_exc())


def parse_japaneseemoticons():
    captions = []
    for page in tqdm(range(1, 20)):
        url = f"https://japaneseemoticons.me/all-japanese-emoticons/{page}"
        html = load_html(url, filename=f"japaneseemoticons_{page}")
        soup = BeautifulSoup(html, 'html.parser')
        for table in soup.find_all("table", class_="copyjava"):
            caption = table.find_previous("h3")
            if not caption or not caption.text or not caption.text.strip():
                continue
            explanation = caption.next_sibling
            try:
                explanation = explanation.strip()
            except:
                explanation = None
            for kaomoji in table.find_all("td"):
                if kaomoji.text.strip():
                    captions.append(Caption(
                        kaomoji=kaomoji.text.strip(),
                        caption=caption.text.strip(),
                        meta={
                            "source": "https://japaneseemoticons.me",
                            "lang": "en",
                            "explanation": explanation
                        }
                    ))
    save_samples(captions, "../data/kaomoji_captions.jsonl", mode="a+")


def parse_kaomoji_ru():
    captions = []
    html = load_html(f"https://kaomoji.ru/en/", filename=f"kaomoji_ru")
    soup = BeautifulSoup(html, 'html.parser')
    for table in soup.find_all("table", class_="table_kaomoji"):
        caption = table.find_previous("h3")
        if not caption or not caption.text or not caption.text.strip():
            continue
        explanation = caption.find_next("p")
        try:
            explanation = explanation.text.strip()
        except:
            explanation = None
        if caption.text.strip() == "Special":
            for tr in table.find_all("tr"):
                kaomoji = tr.find("td")
                caption = kaomoji.find_next("td")
                captions.append(Caption(
                    kaomoji=kaomoji.text.strip(),
                    caption=caption.text.strip(),
                    meta={
                        "source": "https://kaomoji.ru/en/",
                        "lang": "en",
                        "explanation": explanation
                    }
                ))
        else:
            for kaomoji in table.find_all("td"):
                if kaomoji.text.strip():
                    captions.append(Caption(
                        kaomoji=kaomoji.text.strip(),
                        caption=caption.text.strip(),
                        meta={
                            "source": "https://kaomoji.ru/en/",
                            "lang": "en",
                            "explanation": explanation
                        }
                    ))
    save_samples(captions, "../data/kaomoji_captions.jsonl", mode="a+")


def parse_hehuan():
    captions = []
    for page in tqdm(range(1, 75)):
        url = f"http://www.hehuan.co/yanwenzi/list_1_{page}.html"
        html = load_html(url, filename=f"hehuan_{page}")
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all("div", class_="face-item"):
            kaomoji = item.find("div", class_="face")
            caption = item.find("div", class_="bg").find("a")
            captions.append(Caption(
                kaomoji=kaomoji.text.strip(),
                caption=caption.text.strip(),
                meta={
                    "source": "http://www.hehuan.co/yanwenzi",
                    "lang": "chs",
                }
            ))
    save_samples(captions, "../data/kaomoji_captions.jsonl", mode="a+")


def parse_lovelyemoji():
    captions = []
    for page in tqdm(range(1, 8)):
        url = f"https://www.lovelyemoji.com/yanwenzi/index_{page}.html"
        html = load_html(url, filename=f"lovelyemoji_{page}")
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all("div", class_="theme-card"):
            kaomoji = item.find("span", class_="yan")
            caption = item.find("div", class_="card-block")
            captions.append(Caption(
                kaomoji=kaomoji.text.strip(),
                caption=caption.text.strip().replace("颜文字", ""),
                meta={
                    "source": "https://www.lovelyemoji.com/yanwenzi",
                    "lang": "chs",
                }
            ))
    save_samples(captions, "../data/kaomoji_captions.jsonl", mode="a+")


if __name__ == '__main__':
    parse_japaneseemoticons()
    parse_kaomoji_ru()
    parse_hehuan()
    parse_lovelyemoji()
