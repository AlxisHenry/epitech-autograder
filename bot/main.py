import os
import time as t
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

load_dotenv()

service = Service(os.getenv('CHROMEDRIVER_PATH'))
options = webdriver.ChromeOptions()
options.add_argument(os.getenv("CHROME_PROFILE_PATH"))
options.add_argument("--profile-directory=Default")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
driver.get(os.getenv('WEBSITE_URL'))

t.sleep(2)

lastAutograde = driver.find_element(
    By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1").text
[course, createdAt] = lastAutograde.split("\n")
[date, time] = createdAt.split(" ")
[day, month, year] = date.split("/")
[hour, minute] = time.split(":")

# Write to file
with open("./bot/autograder.json", "r") as file:
    data = json.load(file)

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

with open("./bot/autograder.json", "w") as file:
    json.dump(data, file, indent=4)

driver.quit()
