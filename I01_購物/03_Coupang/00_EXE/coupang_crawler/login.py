from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_and_get_driver(email: str, password: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=zh-TW")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://member.tw.coupang.com/login/login.pang")
    time.sleep(2)

    driver.find_element(By.ID, "login-email-input").send_keys(email)
    driver.find_element(By.ID, "login-password-input").send_keys(password)
    driver.find_element(By.CLASS_NAME, "login__button--submit").click()
    time.sleep(5)

    print("✅ 已登入 Coupang")
    return driver
