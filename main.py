import os
import sys
import logging
import shutil
import logging
import requests
import random
import pandas as pd
from time import sleep
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


# directories important for the script
PDF_GENERATOR_DIR = os.getcwd() + "\sample-task-pdf-generator"
LOGPATH = os.getcwd() + "\logs"
DOWNLOAD_DIR = os.getcwd() + "\downloads"

URL = "http://localhost:3002/pdf-panel"


# setting up a logger
if not os.path.exists(LOGPATH):
    os.mkdir(LOGPATH)

log = logging.getLogger("")
log.setLevel(logging.INFO)
format = logging.Formatter("%(levelname)s - %(message)s")

log_file = os.path.join(LOGPATH, "script.log")

if os.path.exists(log_file):
    open(log_file, "w").close()

logging.basicConfig(
    filename=os.path.join(LOGPATH, "script.log"),
    filemode="a",
    format="%(levelname)s - %(message)s",
)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)


# shell commands for running the npm server
def start_server():
    try:
        os.chdir(PDF_GENERATOR_DIR)
        if os.getcwd() == PDF_GENERATOR_DIR:
            os.system("npm install")
            os.system("npm run dev")
            logging.info("Server started successfully!")
    except Exception as e:
        logging.info(e)


def get_browser():
    prefs = {"download.default_directory": DOWNLOAD_DIR}
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return browser
