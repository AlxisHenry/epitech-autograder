import os
import time as t
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

root = False

if "--r" in os.sys.argv:
    root = True

load_dotenv()

chrome_driver_path = os.getenv('CHROMEDRIVER_PATH')

if not root:
    chrome_driver_path = "./bot/" + chrome_driver_path[2:]

service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + os.getenv('CHROME_PROFILE_PATH'))
options.add_argument("--profile-directory=Default")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
driver.get(os.getenv('WEBSITE_URL'))

t.sleep(2)

last_autograde = driver.find_element(
    By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1").text
[course, created_at] = last_autograde.split("\n")
[date, time] = created_at.split(" ")
[day, month, year] = date.split("/")
[hour, minute] = time.split(":")

data = {
    "course": course,
    "date": {
        "day": day,
        "month": month,
        "year": year
    },
    "time": {
        "hour": hour,
        "minute": minute
    }
}

print(data)

with open(root and "./autograder.json" or "./bot/autograder.json", "w") as file:
    json.dump(data, file, indent=4)

driver.quit()
