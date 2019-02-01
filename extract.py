#!/bin/python3
import os

from PyInquirer import style_from_dict, Token, prompt, Separator
from selenium import webdriver
from tqdm import tqdm
import jsbeautifier

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome("./chromedriver", options=options)


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def get_shows(url, show_type="shows", verbose=True):
    driver.get(url)
    show_url_map = []
    shows = driver.find_element_by_id(show_type)
    iterator = tqdm(enumerate(shows.find_elements_by_class_name("box-content")), desc="Extracting shows") if verbose else enumerate(shows.find_elements_by_class_name("box-content"))
    for i, show in iterator:
        if i == 0:
            continue
        try:
            show_section = show.find_element_by_xpath(".//*")
            show_name = show_section.text
            show_url = show_section.get_attribute("href")
            if len(show_name) > 1:
                show_url_map.append((show_name, show_url))
        except:
            pass
    return dict(show_url_map)

def prompt_for_shows(show_url_map):
    questions = [
            {
                "type": "checkbox",
                "qmark": "?",
                "name": "show_name",
                "message": "Pick a show:",
                "choices": [ {"name": show_name} for show_name in show_url_map.keys()]
            }
        ]
    answers = prompt(questions, style=style)
    selected_show_name = answers["show_name"][0]
    url = show_url_map[selected_show_name]
    return url

def get_js(url):
    driver.get(url)
    js = [script.get_attribute("innerHTML") for script in driver.find_elements_by_tag_name("script") if "eval" in script.get_attribute("innerHTML")][0]
    beautified_js = jsbeautifier.beautify(js)
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
    print(run(url))
