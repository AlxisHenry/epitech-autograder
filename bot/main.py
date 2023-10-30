import os
import time as t
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

service = Service(os.getenv('CHROMEDRIVER_PATH'))
options = webdriver.ChromeOptions()
options.add_argument(
    r"--user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format("Alexis"))
options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get("https://my.epitech.eu/")

# Todo: Login

t.sleep(2)

lastAutograde = driver.find_element(
    By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1").text
[course, createdAt] = lastAutograde.split("\n")
[date, time] = createdAt.split(" ")
[day, month, year] = date.split("/")
[hour, minute] = time.split(":")

# Write to file
with open("autograder.json", "r") as file:
    data = json.load(file)

data = {
    "course": course,
    "created_at": createdAt,
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

with open("autograder.json", "w") as file:
    json.dump(data, file, indent=4)
