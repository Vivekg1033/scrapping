import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.youtube.com")

time.sleep(2)
search = driver.find_element(By.NAME, "search_query")
search.send_keys('song')
search.send_keys(Keys.RETURN)
time.sleep(5)

videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
video_list = []
for video in videos[:100]:  
    title = video.get_attribute("title")
    views = video.get_attribute("span")
    url = video.get_attribute("href")
    video_list.append({
            "title": title,  
            "views":views,
            "url": url
        })

for video_info in video_list:
    print(f"Title: {video_info['title']}\nviews: {video_info['views']}\nurl:{video_info['url']}\n")

driver.quit()
