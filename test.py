import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open("data.json","w") as f :
    json.dump([],f)

    def write_json(new_data,filename='data.json'):
        with open(filename,'r+') as file:
            file_data=json.load(file)
            file_data.append(new_data)
            file.seek(0)
            json.dump(file_data,file,indent=4)


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

elem_list = driver.find_element(By.CLASS_NAME, " plp-product-list__products ")

products = elem_list.find_elements(By.CLASS_NAME, 'plp-mastercard ')

for product in products:
    item = WebDriverWait(product, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "plp-price-module__information"))
)
item.click()

WebDriverWait(product, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pip-header-section__title--big"))
)


title = product.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
description = product.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
price = product.find_element(By.CLASS_NAME, "pip-temp-price__integer").text
summary = product.find_element(By.CLASS_NAME, "pip-product-summary__description").text
article = product.find_element(By.CLASS_NAME, "pip-product-identifier__value").text
print(f"Title: '{title}'\nDescription: '{description}'\nPrice: '{price}'\nSummary: '{summary}'\nArticle: '{article}'\n")

write_json({
"title":title,
"deescription":description,
"price":price,
"summary":summary,
"article":article

})

driver.quit()


 