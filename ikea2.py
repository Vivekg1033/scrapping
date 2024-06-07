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
driver.get("https://www.ikea.com/in/en/cat/furniture-sets-55036/?filters=f-special-price%3Atrue")
time.sleep(5)

try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()
except Exception as e:
    print("Cookie consent dialog did not appear or could not be clicked.")


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


info_elements = driver.find_elements(By.CLASS_NAME, "pip-product-information-section")

for info_list in info_elements:
    list_items = info_list.find_elements(By.CLASS_NAME, "pip-list-view-item__title--emphasised")
    for item in list_items:
        print("\n")
        print(item.text)
        item.click()
        time.sleep(2)
        
        details_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-product-details__paragraph"))
        )
        details = ' '.join([detail.text for detail in details_elements])
        print(f"Details: '{details}'")
        
        sub_info = driver.find_elements(By.CLASS_NAME, "pip-modal-body")
        for sub_info_list in sub_info:
            list_sub_items = sub_info_list.find_elements(By.CLASS_NAME, "pip-accordion-item--large.pip-accordion__item")
            for sub_item in list_sub_items:
                print(sub_item.text)
                sub_item.click()
                time.sleep(2)

                content = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-accordion__content--inner-large"))
                )
                for lines_list in content:
                    line = lines_list.find_elements(By.CLASS_NAME, "pip-product-details__container")
                    for l in line:
                        print(l.text)

        try:
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-modal-header__close"))
            )
            close_button.click()
            time.sleep(2)
        except:
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-rr-pip-fe-btn.ugc-rr-pip-fe-btn--small.ugc-rr-pip-fe-btn--icon-primary-inverse"))
            )
            close_button.click()
            time.sleep(2)

driver.quit()



