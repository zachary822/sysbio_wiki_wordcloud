import os
from typing import Generator, Set
from urllib.parse import urldefrag

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from wordcloud import STOPWORDS, WordCloud
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

with open(os.path.join(os.path.dirname(__file__), 'stopwords')) as stopwords_file:
    STOPWORDS |= set(x.strip() for x in stopwords_file.readlines())

__all__ = ['save_word_cloud']


def open_window(driver: WebDriver, url: str) -> None:
    driver.execute_script('open("{}")'.format(url))


def get_links(driver: WebDriver) -> Set[str]:
    links = driver.find_elements_by_xpath("//div[@id='children68296313-0']//a[@href and not(@class)]")

    return {urldefrag(l.get_attribute('href'))[0] for l in links}


def get_text_from_page(driver: WebDriver) -> Generator[str, None, None]:
    texts = driver.find_elements_by_xpath(
        "//div[@id='main-content']/*[not(contains(@class, 'macro') or contains(@class, 'plugin'))]")

    yield from (t.text for t in texts)


def get_text_from_pages(driver: WebDriver) -> Generator[str, None, None]:
    for window in driver.window_handles:
        driver.switch_to.window(window)
        yield from get_text_from_page(driver)


def get_image(driver: WebDriver, width: int = 1920, height: int = 1080) -> Image:
    for link in get_links(driver):
        open_window(driver, link)

    text = ' '.join(get_text_from_pages(driver))

    wordcloud = WordCloud(width=width, height=height, stopwords=STOPWORDS).generate(text)

    return wordcloud.to_image()


def save_word_cloud(name, width: int = 1920, height: int = 1080, *args, **kwargs) -> None:
    """
    Get word cloud from Systems Biology Wiki

    :param name: name of file
    :param width: output file width
    :param height: output file height
    :param args: extra arguments passed to Pillow.Image.save
    :param kwargs: extra arguments passed to Pillow.Image.save
    :return: None
    """
    driver = Chrome(chrome_options=chrome_options)

    driver.get("https://wikis.nyu.edu/display/Vogel/Systems+Biology")

    try:
        image = get_image(driver, width, height)

        image.save(name, *args, **kwargs)
        
    finally:
        driver.quit()
