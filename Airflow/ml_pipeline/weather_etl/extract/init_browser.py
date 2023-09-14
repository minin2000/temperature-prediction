from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os

def init_browser(CONFIG):

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    # If run in Docker
    if os.path.exists('/proc/1/cgroup'):
        options.add_experimental_option("prefs", {"download.default_directory": CONFIG['export_historical_data_path']})
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(20)
    driver.set_page_load_timeout(30)
    driver.maximize_window()

    return driver