# login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("COUPANG_EMAIL")
PASSWORD = os.getenv("COUPANG_PASSWORD")

def login_and_get_driver():
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

    email_input = driver.find_element(By.ID, "login-email-input")
    email_input.send_keys(EMAIL)

    password_input = driver.find_element(By.ID, "login-password-input")
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CLASS_NAME, "login__button--submit")
    login_button.click()

    time.sleep(5)
    return driver
