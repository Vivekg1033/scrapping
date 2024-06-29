import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.williams-sonoma.com/shop/home-furniture/?cm_type=gnav")
time.sleep(5)

try:
    # Find all category elements
    categories_list = driver.find_elements(By.CLASS_NAME, "category-list")

    for category in categories_list:
        # Find the category name
        category_name = category.find_element(By.CLASS_NAME, "heading-label").text
        print(category_name)
        time.sleep(1)

        # Find sub-category elements within the current category context
        sub_categories_list = category.find_elements(By.CLASS_NAME, "flex.flex-col.link-product-name")
        
        print(f"Found {len(sub_categories_list)} sub-categories for {category_name}:")
        for sub_category in sub_categories_list:
            try:
                sub_category_title = sub_category.find_element(By.CLASS_NAME, "text-sm.m-0.text-left.capitalize.tracking-normal").text
                print("    ", sub_category_title)
                
                # # Retrieve the sub-category link
                # try:
                #     sub_category_link = sub_category.find_element(By.TAG_NAME, "a").get_attribute("href")
                #     print("        Link:", sub_category_link)
                # except NoSuchElementException:
                #     print("        Link not found")
                    
            except NoSuchElementException:
                print("    Sub-category title not found")
            
            time.sleep(0.5)
            
except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Quit the driver after processing all categories
    driver.quit()


