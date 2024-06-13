import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import json

# Initialize JSON file if not present
with open("data.json", "w") as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ikea.com/in/en/cat/furniture-sets-55036/?filters=f-special-price%3Atrue")
time.sleep(5)

try:
    # Handle cookie consent if present
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()
except Exception as e:
    print("Cookie consent dialog did not appear or could not be clicked.")

driver.execute_script("window.scrollTo(0, 100);")

# Find all product elements
products = driver.find_elements(By.CLASS_NAME, "plp-price-module__information")

# Limit to the first 10 products if there are more
products = products[:10]

for i in range(len(products)):
    # Find all product elements again in case the page changed
    products = driver.find_elements(By.CLASS_NAME, "plp-price-module__information")
    products[i].click()
    
    # Wait for the product details to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pip-header-section__title--big"))
    )

    # Retrieve product information
    title = driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
    description = driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
    price = driver.find_element(By.CLASS_NAME, "pip-temp-price__integer").text
    summary = driver.find_element(By.CLASS_NAME, "pip-product-summary__description").text
    article = driver.find_element(By.CLASS_NAME, "pip-product-identifier__value").text
    print(f"Title: '{title}'\nDescription: '{description}'\nPrice: '{price}'\nSummary: '{summary}'\nArticle: '{article}'\n")

    # Find all info elements
    info_elements = driver.find_elements(By.CLASS_NAME, "pip-product-information-section")

    for info_list in info_elements:
        list_items = info_list.find_elements(By.CLASS_NAME, "pip-list-view-item__title--emphasised")
        for item in list_items:
            print("\n")
            print(item.text)
            try:
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
                        try:
                            print(sub_item.text)
                            sub_item.click()
                            time.sleep(2)
                            write_json({
                                "title": title,
                                "description": description,
                                "price": price,
                                "summary": summary,
                                "article":article,
                                "item": item.text,
                                "details":details,
                                "sub_item": sub_item.text
                            })
                        except StaleElementReferenceException:
                            print("StaleElementReferenceException: Skipping this sub-item due to stale reference.")
                            continue
            except StaleElementReferenceException:
                print("StaleElementReferenceException: Skipping this item due to stale reference.")
                continue

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

    # Add a small delay before going back to the main page
    time.sleep(2)

    # Go back to the main page to select the next product
    driver.back()
    time.sleep(2)

# Quit the driver after processing all products
driver.quit()
