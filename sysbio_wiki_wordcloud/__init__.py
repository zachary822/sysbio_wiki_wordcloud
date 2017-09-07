import os
from datetime import datetime
from math import floor
from typing import Generator, Set, Union
from urllib.parse import urljoin

import matplotlib
import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup, SoupStrainer

matplotlib.use('Agg')

from wordcloud import STOPWORDS, WordCloud

LINK_URL = "https://wikis.nyu.edu/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position" \
           "&reverse=false&disableLinks=false&expandCurrent=true&hasRoot=true&pageId=20608012&treeId=0&startDepth=0" \
           "&mobile=false&ancestors=68296313&ancestors=20608012&treePageId=68296315&_=1504714430704"

only_wiki_links = SoupStrainer('div', id='children68296313-0')
only_main_content = SoupStrainer('div', id="main-content")
only_comments = SoupStrainer('div', id='comments-section')

with open(os.path.join(os.path.dirname(__file__), 'stopwords')) as stopwords_file:
    STOPWORDS |= set(x.strip() for x in stopwords_file.readlines())

__all__ = ['save_word_cloud']


def get_links(session: requests.Session) -> Set[str]:
    link_page = session.get(LINK_URL)

    link_soup = BeautifulSoup(link_page.content, 'lxml', parse_only=only_wiki_links)

    return {urljoin(LINK_URL, l['href']) for l in link_soup.find_all('a', attrs={'class': False})}


def get_text_from_page(resp: requests.Response) -> str:
    soup = BeautifulSoup(resp.content, 'lxml', parse_only=only_main_content)
    return soup.get_text()


def get_comments_from_page(resp: requests.Response) -> str:
    soup = BeautifulSoup(resp.content, 'lxml', parse_only=only_comments)

    return ' '.join(c.get_text() for c in soup.find_all('div', attrs={'class': 'comment-content'}))


def get_text_from_pages(session: requests.Session, return_link: bool = False, comment: bool = False) -> \
        Generator[str, None, None]:
    for link in get_links(session):
        if comment:
            result = get_comments_from_page(session.get(link))
        else:
            result = get_text_from_page(session.get(link))

        if return_link:
            result = result, link

        yield result


def get_wordcloud_image(width: int = 1920, height: int = 1080, comment: bool = False) -> Image:
    with requests.Session() as session:
        text = ' '.join(get_text_from_pages(session, comment=comment))

    wordcloud = WordCloud(width=width, height=height, stopwords=STOPWORDS).generate(text)

    return wordcloud.to_image()


def draw_timestamp(image: Image, size: Union[int, None] = None) -> Image:
    date_str = datetime.now().isoformat()
    draw = ImageDraw.Draw(image)

    i_width, i_height = image.size

    if size is None:
        size = floor(i_height * 0.02)

    font = ImageFont.truetype("Hack-Regular.ttf", size=size)

    f_width, f_height = draw.textsize(date_str, font=font)

    x = i_width - f_width - size
    y = i_height - f_height - size

    draw.text((x, y), date_str, font=font)

    return image


def save_word_cloud(name, width: int = 1920, height: int = 1080, timestamp: bool = True, comment: bool = False,
                    *args, **kwargs) -> None:
    """
    Get word cloud from Systems Biology Wiki

    :param name: name of file
    :param width: output file width
    :param height: output file height
    :param timestamp: include timestamp
    :param comment: use comments instead of wiki page
    :param args: extra arguments passed to Pillow.Image.save
    :param kwargs: extra arguments passed to Pillow.Image.save
    :return: None
    """
    image = get_wordcloud_image(width, height, comment=comment)

    if timestamp:
        draw_timestamp(image)

    image.save(name, *args, **kwargs)
