#!/bin/python3
from selenium import webdriver
import jsbeautifier

def get_js(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    js = [script.get_attribute("innerHTML") for script in driver.find_elements_by_tag_name("script") if "eval" in script.get_attribute("innerHTML")][0]
    beautified_js = jsbeautifier.beautify(js)
    return beautified_js

def extract_m3u8(url):
    text = get_js(url)
    url = text.split(";")[-3].split("'")[1][:-1]
    return url
