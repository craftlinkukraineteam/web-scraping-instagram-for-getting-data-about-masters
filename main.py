import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_profile_path = r"C:/Users/nazar/AppData/Local/Google/Chrome/User Data"

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument("profile-directory=Default")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)
wait = WebDriverWait(driver, 20)

def search_profiles(query):
    search_box = wait.until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search input']"))
    )
    search_box.send_keys(query)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    profiles = set()

    for _ in range(5):
        links = driver.find_elements(By.XPATH, "//a[contains(@href,'/') and not(contains(@href,'explore'))]")
        for link in links:
            href = link.get_attribute("href")
            if href and href.count("/") == 3:
                profiles.add(href)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    return list(profiles)

def parse_profile(url):
    driver.get(url)
    wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "header")))
    username = url.rstrip("/").split("/")[-1]

    try:
        name = driver.find_element(By.XPATH, "//h1").text
    except:
        name = ""

    try:
        bio = driver.find_element(By.XPATH, "//div[@data-testid='user-bio']").text
    except:
        bio = ""

    try:
        followers = driver.find_element(
            By.XPATH, "//a[contains(@href,'followers')]/span"
        ).get_attribute("title")
    except:
        followers = ""

    return {
        "username": username,
        "name": name,
        "bio": bio,
        "followers": followers
    }

driver.get("https://www.instagram.com/")

profiles = search_profiles("візажист Харків")

data = []
for profile in profiles[:20]:
    try:
        data.append(parse_profile(profile))
    except Exception as e:
        print(f"Помилка для {profile}: {e}")

df = pd.DataFrame(data)
df.to_excel("instagram_parser.xlsx", index = False)

driver.quit()
