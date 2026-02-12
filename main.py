from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

USERNAME = "craftlinkukraineteam"
PASSWORD = "Oo681713OoOoOoOoOo"

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

def login():
    driver.get("https://www.instagram.com")
    username_input = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "username")))
    username_input.send_keys(USERNAME)
    password_input = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "password")))
    password_input.send_keys(PASSWORD + Keys.ENTER)
login()

search = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
search.send_keys("візажист Харків")
time.sleep(2)
search.send_keys(Keys.ENTER)
time.sleep(2)
search.send_keys(Keys.ENTER)

profiles = set()

for _ in range(5):
    links = driver.find_elements(By.XPATH, "//a[contains(@href,'/')]")
    for link in links:
        href = link.get_attribute("href")
        if href and href.count("/") == 4:
            profiles.add(href)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

data = []
for profile in list(profiles)[:20]:
    driver.get(profile)
    time.sleep(4)

    try:
        username = profile.split("/")[-2]

        try:
            name = driver.find_element(By.TAG_NAME, "h2").text
        except:
            name = ""

        try:
            bio = driver.find_element(By.XPATH, "//div[contains(@class,'_aa_c')]").text
        except:
            bio = ""

        try:
            followers = driver.find_element(By.XPATH, "//ul/li[2]/a/span").get_attribute("title")
        except:
            followers = ""

        data.append({
            "username": username,
            "name": name,
            "bio": bio,
            "followers": followers
        })
    except Exception as e:
        print(f"Помилка для {profile}: {e}")

df = pd.DataFrame(data)
df.to_excel("instagram_parser_for_getting_data_about_masters.xlsx", index = False)
df.to_excel("instagram_parser_for_getting_data_about_masters.xlsx", index = False)

driver.quit()
