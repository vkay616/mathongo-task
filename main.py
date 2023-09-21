import os
import sys
import logging
import logging
from threading import Thread
import json
import pyautogui
from time import sleep
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from PyPDF2 import PdfWriter


# directories important for the script
PDF_GENERATOR_DIR = os.getcwd() + "\sample-task-pdf-generator"
LOGPATH = os.getcwd() + "\logs"
DOWNLOAD_DIR = os.getcwd() + "\downloads"
DB_DIR = PDF_GENERATOR_DIR + "\db"

URL = "http://localhost:3002/pdf-panel"

# all files in db folder
FILESNAMES = [f[:-5] for f in os.listdir(DB_DIR)]

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


# setting up a log
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


# starting server in a separate thread
npm_server_thread = Thread(target=start_server)
npm_server_thread.start()
sleep(7)


# function to get driver
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


# function to download questions and solutions pdf files
def download_files(driver: webdriver.Chrome, file: str):
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(URL)
        main_tab = driver.current_window_handle
        wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//*[@id="jsonFile"]'
                ))
            ).send_keys(file)
        wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                '/html/body/section/div/div[3]/div/a'
                ))
            ).click()
        wait.until(EC.number_of_windows_to_be(3))
        sleep(20)
        for tab in driver.window_handles:
            if len(driver.window_handles) == 1:
                break
            if tab != main_tab:
                driver.switch_to.window(tab)
                logging.info(driver.title)
                driver.execute_script("window.print();")
                sleep(5)
                filename = f"{DOWNLOAD_DIR}\{file}\{driver.title}"
                pyautogui.typewrite(filename)
                pyautogui.hotkey("enter")
                sleep(2)
                driver.close()
                driver.switch_to.window(main_tab)
                continue
        sleep(2)


    except Exception as e:
        logging.info(e)


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