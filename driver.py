from http import client as httplib
import socket

from selenium.webdriver.remote.command import Command
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
try:
    driver = webdriver.Chrome(options=options)
except:
    pass
try:
    driver = webdriver.Chrome("./chromedriver", options=options)
except:
    import AutoChromedriver
    AutoChromedriver.download_chromedriver()
    driver = webdriver.Chrome("./chromedriver", options=options)

def is_alive(driver):
    try:
        driver.execute(Command.STATUS)
        return True
    except (socket.error, httplib.CannotSendRequest):
        return False

def quitdriver():
    driver.quit()

import atexit
atexit.register(quitdriver)
