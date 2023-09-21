# importing required libraries
import os
import sys
import logging
from threading import Thread
import json
import pyautogui
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from PyPDF2 import PdfWriter


# directories important for the script
PDF_GENERATOR_DIR = os.getcwd() + "\sample-task-pdf-generator" # directory for the npm package.json
LOGPATH = os.getcwd() + "\logs" # directory for the log
DOWNLOAD_DIR = os.getcwd() + "\downloads" # directory for the downloads
DB_DIR = PDF_GENERATOR_DIR + "\db" # directory for the json files

URL = "http://localhost:3002/pdf-panel" # main url for the server

# creating a list containing all files inside db folder
FILESNAMES = [f[:-5] for f in os.listdir(DB_DIR)]

# settings for the Chrome WebDriver, to make the Save as PDF option default on Print Page
SETTINGS = {
    "appState": {
        "recentDestinations": [{
            "account": "",
            "id": "Save as PDF",
            "origin": "local"
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }  
}

# setting up downloads folder
for file in FILESNAMES:
    if not os.path.exists(f"{DOWNLOAD_DIR}\{file}"):
        os.mkdir(f"{DOWNLOAD_DIR}\{file}")


# setting up the log folder
if not os.path.exists(LOGPATH):
    os.mkdir(LOGPATH)

# setting up the logger
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

# function to run shell commands for running the npm server
def start_server():
    try:
        os.chdir(PDF_GENERATOR_DIR)
        if os.getcwd() == PDF_GENERATOR_DIR:
            os.system("npm install")
            os.system("npm run dev")
            logging.info("Server started successfully!")
    except Exception as e:
        logging.info(e)


# starting server in a separate thread
npm_server_thread = Thread(target=start_server)
npm_server_thread.start()
sleep(7)


# function to get the Chrome WebDriver with desired settings
def get_driver():
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "savefile.default_directory": DOWNLOAD_DIR,
        "printing.print_preview_sticky_settings.appState": json.dumps(SETTINGS),
        }
    
    chrome_options = Options()

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return driver


# function to download questions and solutions pdf files, takes a driver and a file name (should be from db folder) as input
def download_files(driver: webdriver.Chrome, file: str):
    # initializing wait time
    wait = WebDriverWait(driver, 20)
    try:
        # open URL in driver
        driver.get(URL)
        # keeping track of the main tab
        main_tab = driver.current_window_handle
        # entering file name (from db folder) to the form
        wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//*[@id="jsonFile"]'
                ))
            ).send_keys(file)
        # clicking on generate button
        wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                '/html/body/section/div/div[3]/div/a'
                ))
            ).click()
        # waiting for the popup tabs to open
        wait.until(EC.number_of_windows_to_be(3))
        # waiting 20 seconds as instructed for the tabs to load images
        sleep(20)
        # traversing through the multiple tabs opened in browser
        for tab in driver.window_handles:
            if len(driver.window_handles) == 1:
                break
            if tab != main_tab:
                # switching to a different tab from the main one
                driver.switch_to.window(tab)
                # logging the info
                logging.info("Saving PDF of " + driver.title + " tab")
                # printing the webpage to save as PDF
                driver.execute_script("window.print();")
                # waiting for the save as file prompt opens successfully
                sleep(5)
                # the file will be saved as 
                filename = f"{DOWNLOAD_DIR}\{file}\{driver.title}"
                # using pyautogui to interact with the save as file prompt
                pyautogui.typewrite(filename)
                pyautogui.hotkey("enter")
                sleep(2)
                # closing the current tab
                driver.close()
                # switching to main tab
                driver.switch_to.window(main_tab)

                continue
        sleep(2)


    except Exception as e:
        logging.info(e)

# function to merge the question and solutions pdf
def merge_pdf(directory: str):
    merger = PdfWriter()
    files = [f"{directory}\question_marks.pdf", f"{directory}\solution_marks.pdf"]
    for file in files:
        merger.append(file)
    
    merger.write(f"{directory}.pdf")
    merger.close()
        

driver = get_driver()

for file in FILESNAMES:
    try:
        download_files(driver, file)
    
    except Exception as e:
        logging.info(e)


for file in FILESNAMES:
    merge_pdf(f"{DOWNLOAD_DIR}\{file}")