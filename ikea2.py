import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ikea.com/in/en/cat/lower-price/?sort=RATING&filters=f-subcategories%3Afu001")
time.sleep(5)

driver.execute_script("window.scrollTo(0, 100);")

product = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "plp-price-module__information"))
)
product.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pip-header-section__title--big"))
)


title = driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
description = driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
price = driver.find_element(By.CLASS_NAME, "pip-temp-price__integer").text
summary = driver.find_element(By.CLASS_NAME, "pip-product-summary__description").text
article = driver.find_element(By.CLASS_NAME, "pip-product-identifier__value").text

print(f"Title: '{title}'\nDescription: '{description}'\nPrice: '{price}'\nSummary: '{summary}'\nArticle: '{article}'\n")


info_elements = driver.find_elements(By.CLASS_NAME, "js-product-information-section.pip-product-information-section")

for info_list in info_elements:  
    list_items = info_list.find_elements(By.CLASS_NAME, "pip-list-view-item__title.pip-list-view-item__title--emphasised")
    for item in list_items:
        print(item.text)

driver.quit()



