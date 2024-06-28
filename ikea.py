import sys
import io
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

# Initialize JSON file if not present
with open("data.json", "w") as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def main_details(driver):
    """Retrieve product details and return as a dictionary."""
    try:
        title = driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
        description = driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
        price = driver.find_element(By.CLASS_NAME, "pip-temp-price__integer").text
        summary = driver.find_element(By.CLASS_NAME, "pip-product-summary__description").text
        article = driver.find_element(By.CLASS_NAME, "pip-product-identifier__value").text
        img = driver.find_element(By.CLASS_NAME, "pip-image").get_attribute("src")
        link = driver.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        print(f"Title: '{title}'\nDescription: '{description}'\nPrice: '{price}'\nSummary: '{summary}'\nArticle: '{article}'\nimage: '{img}'\nlink '{link}'\n")
        
        return {
            "title": title,
            "description": description,
            "price": price,
            "summary": summary,
            "article": article,
            "img": img,
            "link": link
        }
    except NoSuchElementException as e:
        print(f"Failed to retrieve product details: {str(e)}")
        return None

def reviews(driver):
    rev_list = []
    try:
        # Wait for the 'Details' section button and click it
        section4 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pip-list-view-item.pip-chunky-header__reviews"))
        )
        section4.click()
        print("Clicked on 'Reviews' item.")
        time.sleep(2)  # Adjust this wait time if needed

        # Wait for the modal to appear
        rev_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ugc-rr-pip-fe-modal-body"))
        )
        print("Modal found.")
        
        # Extract reviews
        reviews = rev_modal.find_elements(By.CLASS_NAME, "ugc-rr-pip-fe-overall-rating")
        for review in reviews:
            try:
                rating = review.find_element(By.CLASS_NAME, "text.text--heading-xl").text
                number = review.find_element(By.CLASS_NAME, "ugc-rr-pip-fe-text.ugc-rr-pip-fe-text--body-m.ugc-rr-pip-fe-overall-rating__value-reviews").text
                rev_list.append({
                    "title": section4.text,
                    "stars": rating,
                    "based on this number of reviews": number
                })
            except NoSuchElementException as e:
                print(f"Error extracting review details: {str(e)}")
                continue

        # Close the modal if it's open
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-modal-header__close"))
            )
            close_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            pass

    except TimeoutException as e:
        print(f"Timeout while waiting for 'Reviews' section: {str(e)}")

    except Exception as e:
        import traceback
        print(f"Unexpected error occurred in 'reviews': {str(e)}")
        traceback.print_exc()

    return rev_list


    


def measurements(driver):
    mm_list = []

    try:
        # Find and click the 'Details' section button
        section3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pip-list-view-item.pip-chunky-header__measurement"))
        )
        section3.click()
        print("Clicked on 'Details' item.")
        time.sleep(2)  # Adjust this wait time if needed

        # Wait for the modal to appear
        wi_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pip-modal-body"))
        )
        print("Modal found.")

        # Get the dimensions text
        text_elements = wi_modal.find_elements(By.CLASS_NAME, "pip-product-dimensions__dimensions-container")
        text = ' '.join([element.text for element in text_elements])

        # Get the image URL
        img = wi_modal.find_element(By.CLASS_NAME, "pip-image").get_attribute("src")

        # Click on the 'Package Dimensions' section
        package = WebDriverWait(wi_modal, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pip-accordion__heading.pip-accordion-item-header.pip-accordion-item-header--large"))
        )
        package.click()
        time.sleep(2)  # Adjust this wait time if needed

        # Get the package dimensions text
        pack_text_elements = wi_modal.find_elements(By.CLASS_NAME, "pip-product-dimensions__dimensions-container")
        pack_text = ' '.join([element.text for element in pack_text_elements])

        mm_list.append({
            "title": section3.text,
            "dimensions": text,
            "image": img,
            "sub_details": pack_text
        })

        # Close the modal if it's open
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-modal-header__close"))
            )
            close_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            pass

    except NoSuchElementException as e:
        print(f"Error retrieving 'Measurements' details: {str(e)}")

    except Exception as e:
        print(f"Unexpected error occurred in 'measurements': {str(e)}")

    return mm_list


def whats_included(driver):
    wi_list = []

    try:
        # Find and click the 'What's Included' section button
        section2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pip-list-view-item.pip-chunky-header__included-products"))
        )
        section2.click()
        print("Clicked on 'What's Included' item.")
        time.sleep(2)  # Adjust this wait time if needed

        # Wait for the modal to appear
        wi_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pip-modal-body"))
        )
        print("Modal found.")

        # Get subtitles
        sub_titles = wi_modal.find_elements(By.CLASS_NAME, "pip-included-products__subtitle")
        print(f"Found {len(sub_titles)} subtitle elements.")

        # Get the list of items
        list_items = wi_modal.find_elements(By.CLASS_NAME, "pip-included-products__container")
        img_list = []
        for item in list_items:
            img = item.find_element(By.CLASS_NAME, "pip-image").get_attribute("src")
            text_elements = item.find_elements(By.CLASS_NAME, "pip-product-card__info-container")
            text = ' '.join([text.text for text in text_elements])
            img_list.append({
                "image": img,
                "sub_details": text
            })

        wi_list.append({
            "title": section2.text,
            "details": ' '.join([subtitle.text for subtitle in sub_titles]),
            "image": img_list
        })

        # Close the modal if it's open
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-modal-header__close"))
            )
            close_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            pass

    except TimeoutException:
        print("TimeoutException: 'What's Included' section not clickable or modal not found. Proceeding without this section.")

    except NoSuchElementException as e:
        print(f"Error retrieving 'What's Included' details: {str(e)}")

    except Exception as e:
        print(f"Unexpected error occurred in 'whats_included': {str(e)}")

    return wi_list


def product_details(driver):
    """Retrieve additional product information."""
    pd_list = []

    try:
        # Find and click the 'Details' section button
        section1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pip-list-view-item.pip-chunky-header__details.js-chunky-header__details"))
        )
        section1.click()
        print("Clicked on 'Details' item.")
        time.sleep(2)  # Adjust this wait time if needed

        # Retrieve details
        details_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-product-details__paragraph"))
        )
        details = ' '.join([detail.text for detail in details_elements])

        # Retrieve sub-items
        gtk_list = []
        sub_info = driver.find_elements(By.CLASS_NAME, "pip-modal-body")
        for sub_info_list in sub_info:
            list_sub_items = sub_info_list.find_elements(By.CLASS_NAME, "pip-accordion-item--large.pip-accordion__item")
            for sub_item in list_sub_items:
                try:
                    sub_item.click()
                    time.sleep(2)
                    # sub_details_elements = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-product-details__container"))
                    # )
                    # sub_details = ' '.join([sub_detail.text for sub_detail in sub_details_elements])
                    gtk_list.append({
                        "sub_item": sub_item.text
                    })
                except StaleElementReferenceException:
                    print("StaleElementReferenceException: Skipping this sub-item due to stale reference.")
                    continue

        pd_list.append({
            "title": section1.text,
            "details": details,
            "sub_items": gtk_list
        })

        # Close the modal if it's open
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pip-btn.pip-btn--small.pip-btn--icon-primary-inverse.pip-modal-header__close"))
            )
            close_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            pass

    except NoSuchElementException:
        print("No pip-list-view-item__title--emphasised found in the first info_list.")

    except Exception as e:
        print(f"Unexpected error occurred in 'product_details': {str(e)}")

    return pd_list


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ikea.com/in/en/cat/lower-price/?sort=RATING&filters=f-subcategories%3Afu001")
time.sleep(5)

try:
    # Handle cookie consent if present
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()
except TimeoutException:
    print("Cookie consent dialog did not appear or could not be clicked.")

# # Click "Show more" button until it's no longer clickable
# while True:
#     try:
#         smbtn = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".plp-btn.plp-btn--small.plp-btn--secondary"))
#         )
#         smbtn.click()
#         time.sleep(2)  # Give time for more products to load
#     except TimeoutException:
#         print("No more 'Show more' button to click.")
#         break

# Find all product elements
products = driver.find_elements(By.CLASS_NAME, "plp-price-module__information")

# Limit to the first 10 products if there are more

products = products[:2]
for i in range(len(products)):
    try:
        # Find all product elements again in case the page changed
        products = driver.find_elements(By.CLASS_NAME, "plp-price-module__information")
        
        # Scroll the product element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", products[i])
        time.sleep(1)
        
        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", products[i])
    except ElementClickInterceptedException:
        print(f"Element {i+1} is not clickable.")
        continue
    
    # Wait for the product details to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pip-header-section__title--big"))
        )
    except TimeoutException:
        print("Product details did not load in time.")
        driver.back()
        continue
    
    # Extract main product details
    details = main_details(driver)
    
    # Extract additional product information
    additional_info1 = product_details(driver)
    additional_info2 = whats_included(driver)
    additional_info3 = measurements(driver)
    additional_info4 = reviews(driver)
    
    # Combine additional information
    details["additional_info"] =additional_info1+additional_info2+additional_info3+additional_info4
    
    # Write data to JSON
    write_json(details)
    
    # Add a small delay before going back to the main page
    time.sleep(2)
    
    # Go back to the main page to select the next product
    driver.back()
    time.sleep(2)

# Quit the driver after processing all products
driver.quit()










