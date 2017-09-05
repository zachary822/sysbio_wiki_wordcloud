import argparse
from typing import Generator
from urllib.parse import urldefrag

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from wordcloud import WordCloud


def get_text_from_page(driver: WebDriver) -> Generator[str, None, None]:
    texts = driver.find_elements_by_xpath(
        "//div[@id='main-content']/*[not(contains(@class, 'macro') or contains(@class, 'plugin'))]")

    for t in texts:
        yield t.text


def get_text_from_pages(driver: WebDriver) -> Generator[str, None, None]:
    for window in driver.window_handles:
        driver.switch_to.window(window)
        yield from get_text_from_page(driver)


def save_word_cloud(name):
    driver = Chrome()

    driver.get("https://wikis.nyu.edu/display/Vogel/Systems+Biology")

    try:
        links = driver.find_elements_by_xpath("//div[@id='children68296313-0']//a[@href and not(@class)]")

        for link in {urldefrag(l.get_attribute('href'))[0] for l in links}:
            driver.execute_script('open("{}")'.format(link))

        text = ' '.join(get_text_from_pages(driver))

        wordcloud = WordCloud(width=1920, height=1080).generate(text)

        image = wordcloud.to_image()

        image.save(name, optimize=True)

    except NoSuchElementException:
        pass

    driver.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output file name.", default="wordcloud.png")

    args = parser.parse_args()

    save_word_cloud(args.output)


if __name__ == "__main__":
    main()
