from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# navigate to specified url, most work platforms keep data in url params.
driver.get("https://it.pracuj.pl/praca/frontend;kw/it%20-%20rozw%C3%B3j%20oprogramowania;cc,5016")

# wait for cookiesm if they popup, accept them
WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-test='button-submitCookie']"))
    )

cookie_element = driver.find_element(By.XPATH, "//button[@data-test='button-submitCookie']")

if cookie_element.is_displayed():
    print('clicking cookies')
    cookie_element.click()

# wait for section-offers, main div that contains all matching/related job offers
WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-test='section-offers']"))
    )

offers_element = driver.find_element(By.XPATH, "//div[@data-test='section-offers']")
children_elements = offers_element.find_elements(By.XPATH, ".//div/div/h2[@data-test='offer-title']")

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