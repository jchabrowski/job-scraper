from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from termcolor import cprint

# XPATHS ARE STORED IN .ENV, SO THE JOB PORTALS I SCRAPE ARE NOT THAT OBVIOUS
load_dotenv()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

print_red_on_cyan = lambda x: cprint(x, "red", "on_cyan")
print_red_on_yellow = lambda x: cprint(x, "red", "on_yellow")
print_black_on_red = lambda x: cprint(x, "black", "on_red")

# navigate to specified url, most work platforms keep data in url params.
driver.get(os.getenv("BASE_URL"))

def check_cookies():
    # wait for cookies - if they pop up, accept them
    try:
        WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, os.getenv("COOKIE_XPATH")))
            )

        cookie_element = driver.find_element(By.XPATH, os.getenv("COOKIE_XPATH"))

        if cookie_element.is_displayed():
            print('clicking cookies')
            cookie_element.click()

        print('waiting for 3 seconds')
        driver.implicitly_wait(3)

    except TimeoutException:
        print("Cookies not found with specified timeout")

# access each page once and print all offers
def main_loop(i):
    check_cookies()

    if (i > 1):
        base_url = os.getenv('BASE_URL')
        new_url = f"{base_url}?pn={i}"
        driver.get(new_url)

        print(f"Currently navigated to page number {i}")
        print(f"-----Sleeping for 3 sec----- on {i} main function call")
        time.sleep(3)

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH")))
    )

    offers_element = driver.find_element(By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH"))

    child_elements =  offers_element.find_elements(By.XPATH, "./*")

    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, os.getenv("OFFER_TITLE_ELEMENT")))
        )

    my_keywords = ['fullstack', 'full stack', 'frontend', 'react', 'javascript', 'js', 'node', 'next', 'next.js']
    restricted_keywords = ['junior', 'qa', 'tester', 'java', 'lead', 'leader', 'staff']

    for index, child in enumerate(child_elements):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH")))
        )
        
        offers_element = driver.find_element(By.XPATH, os.getenv("OFFERS_CONTAINER_XPATH"))

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, os.getenv("OFFER_TITLE_ELEMENT")))
        )

        child_elements =  offers_element.find_elements(By.XPATH, "./*")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, os.getenv("SINGLE_OFFER_TITLE")))
            )

            title = child.find_element(By.XPATH, os.getenv("SINGLE_OFFER_TITLE")).text

        except NoSuchElementException:
            print(f'Child element {index} is missing the offer title.')
            continue

        try:
            salary = child.find_element(By.XPATH, os.getenv("SINGLE_OFFER_SALARY")).text

        except NoSuchElementException:
            print_red_on_yellow(f'Child element {index} with title <<<{title}>>> is missing salary.')
            continue

        try:
            company_name_elements = child.find_elements(By.XPATH, os.getenv("SINGLE_OFFER_COMPANY_NAME"))
            company_name = company_name_elements[1].text

        except NoSuchElementException:
            print(f'Child element {index} with title <<<{title}>>> is missing company name.')
            continue
            # anchor_tag_value = driver.find_element(By.XPATH, './/a[@data-test="link-offer"]').get_attribute('href')

        try:
            is_restricted = False

            for keyword in restricted_keywords:
                if keyword in title.lower():
                    print_black_on_red(f'RESTRICTED KEYWORD ----- {keyword} >>> in <<<{title}>>> <<<{salary}>>> at <<{company_name}>>')
                    is_restricted = True
                    break

            if is_restricted:
                continue

            for keyword2 in my_keywords:
                if keyword2 in title.lower():
                    print_red_on_cyan(f'Found <<<{title}>>> <<<{salary}>>> at <<{company_name}>>')
        
            # matched_offers.add({title, salary, company_name})

        except Exception as e:
            print(f'ERROR PROCESSING CHILD ELEMENT: {e}')

WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, os.getenv("MAX_PAGINATION")))
    )

offer_pages_amount = int(driver.find_element(By.XPATH, os.getenv("MAX_PAGINATION")).text)

print(f"I can see there are {offer_pages_amount} pages")

for i in range(1, offer_pages_amount):
    main_loop(i)

time.sleep(3)

print('-------------------------------------------')
print('sleeping for 120 sec')

time.sleep(120)

driver.quit()

