from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# driver.get("https://justjoin.it/all-locations/javascript/remote_yes")
# driver.get("https://pracuj.pl")
# driver.get("https://pracuj.pl")
driver.get("https://it.pracuj.pl/praca/frontend;kw/it%20-%20rozw%C3%B3j%20oprogramowania;cc,5016")

# wait for cookies
WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-test='button-submitCookie']"))
    )

# type 'Frontend into search and perform search'
# search_element = driver.find_element(By.XPATH, "//input[@name='kw']")
# search_element.send_keys('Frontend')

# search_button = driver.find_element(By.XPATH, "//span[@class='core_ig18o8w size-xlarge position-left']")
# search_button.click()

# cookie_element = driver.find_element(By.CLASS_NAME, "size-medium variant-primary core_b1fqykql").click()
cookie_element = driver.find_element(By.XPATH, "//button[@data-test='button-submitCookie']")
# search_element = driver.find_element(By.XPATH, "//input[@name='kw']")
# search_button = driver.find_element(By.XPATH, "//span[@class='core_ig18o8w size-xlarge position-left']")

# offers_section = driver.find_element(By.XPATH, "//div[@data-test='section-offers']")

if cookie_element.is_displayed():
    print('clicking cookies')
    cookie_element.click()

WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-test='section-offers']"))
    )

offers_element = driver.find_element(By.XPATH, "//div[@data-test='section-offers']")

my_keywords = ['Fullstack', 'fullstack', 'FullStack', 'Full Stack', 'Full stack', 'Frontend', 'frontend', 'React', 'react', 'Javascript', 'javascript', 'js']
matching_elements = driver.find_elements(By.XPATH, f"//h2[contains(text(), '{keyword}')]")

# Get offers with keywords //h2[contains(text(), 'Fullstack')]

print('sleeping')
time.sleep(5)

for element in matching_elements:
    print(element.text)


print('after sleep')

# print(search_element)

# cookie_element.click()
# keyword_element.send_keys('Frontend' + Keys.Enter)



time.sleep(120)

# driver.quit()