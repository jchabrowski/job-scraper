from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# XPATHS ARE STORED IN .ENV, SO THE JOB PORTALS I SCRAPE ARE NOT THAT OBVIOUS
load_dotenv()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# navigate to specified url, most work platforms keep data in url params.
driver.get(os.getenv("STARTING_PAGE"))

# wait for cookiesm if they popup, accept them
WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, os.getenv("COOKIE_XPATH")))
    )

cookie_element = driver.find_element(By.XPATH, os.getenv("COOKIE_XPATH"))

if cookie_element.is_displayed():
    print('clicking cookies')
    cookie_element.click()

# wait for the main div that contains all matching/related job offers
WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH")))
    )

offers_element = driver.find_element(By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH"))
children_elements = offers_element.find_elements(By.XPATH, os.getenv("CHILDREN_ELEMENTS"))

print(f"Scrapping: {len(children_elements)} offers" )

my_keywords = ['fullstack', 'full stack', 'frontend', 'react', 'javascript', 'js', 'node', 'next', 'next.js']

matched_offers = set()

for el in children_elements:
    print(el.text)
    for keyword in my_keywords:
        if keyword in el.text.lower():
            matched_offers.add(el.text)
            print(f'Found  <<<{keyword.upper()}>>> matching in ....... <<<{el.text.upper()}>>>')


time.sleep(10)

print(matched_offers)

print('sleeping')

time.sleep(120)

driver.quit()