#!/usr/bin/python3
import os

import jsbeautifier

from driver import driver, is_alive
from prompt import get_shows, prompt_for_shows

def get_js(url):
    driver.get(url)
    js = [script.get_attribute("innerHTML") for script in driver.find_elements_by_tag_name("script") if "eval" in script.get_attribute("innerHTML")][0]
    beautified_js = jsbeautifier.beautify(js)
    if is_alive(driver):
        driver.quit()

    return beautified_js

def extract_m3u8(url):
    text = get_js(url)
    url = text.split(";")[-3].split("'")[1][:-1]
    return url

def run(url, show_type="shows"):
    show_url_map = get_shows(url, show_type)
    show_url = prompt_for_shows(show_url_map)
    return extract_m3u8(show_url)


if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(extract_m3u8(url))
