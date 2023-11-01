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

browser = os.getenv('BROWSER')

driver_path = os.getenv('DRIVER_PATH')

if not root:
    driver_path = "./bot/" + driver_path[2:]

service = Service(driver_path)

if browser == "chrome":
    options = webdriver.ChromeOptions()
else:
    options = webdriver.EdgeOptions()

options.add_argument("--user-data-dir=" + os.getenv('PROFILE_PATH'))
options.add_argument("--profile-directory=Defadult")
options.add_argument("--headless")

if browser == "edge":
    options.add_argument('log-level=3')

if browser == "chrome":
    driver = webdriver.Chrome(service=service, options=options)
else:
    driver = webdriver.Edge(service=service, options=options)

driver.get(os.getenv('WEBSITE_URL'))

t.sleep(2)

if driver.find_elements(By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1") == []:
    if driver.find_elements(By.XPATH, "/html/body/div/div/a/span") != []:
        driver.find_element(By.XPATH, "/html/body/div/div/a/span").click()
        t.sleep(2)
    else:
        driver.quit()
        exit()

if driver.find_elements(By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1") != []:
    last_autograde = driver.find_element(
        By.XPATH, "/html/body/div/div/main/div[2]/div[1]/div/div[1]/h1").text
    
    driver.quit()

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
