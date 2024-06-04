import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ikea.com/in/en/cat/lower-price/?sort=RATING&filters=f-subcategories%3Afu001")

try:
    # Close the cookie consent dialog if it appears
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_button.click()
    except Exception as e:
        print("Cookie consent dialog did not appear or could not be clicked.")

    # Scroll down a bit to ensure elements load
    driver.execute_script("window.scrollTo(0, 100);")

    # Wait for the product to be present in the DOM and visible
    product = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "plp-price-module__information"))
    )
    product.click()

    # Wait for the product details to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pip-header-section__title--big"))
    )

    # Extract title, description, and price
    title = driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
    description = driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
    price = driver.find_element(By.CLASS_NAME, "pip-temp-price__integer").text

    # Print the extracted information
    print(f"Title: '{title}'\nDescription: '{description}'\nPrice: '{price}'\n")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
