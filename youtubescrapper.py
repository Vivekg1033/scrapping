from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

driver = webdriver.Chrome()



driver.get("https://www.youtube.com")


time.sleep(5)

search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys('song')
search_box = driver.find_element(By.ID, "search-icon-legacy")
search_box.click()

time.sleep(5)

videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')

video_info_list = []

for video in videos[:100]:  # Limiting to first 10 results for example
    title = video.get_attribute("title")
    url = video.get_attribute("href")
    video_info_list.append({
        "title": title,
        "url": url
    })

# Print the collected information
for video_info in video_info_list:
    print(f"Title: {video_info['title']}\nURL: {video_info['url']}\n")

# Close the WebDriver
driver.quit()