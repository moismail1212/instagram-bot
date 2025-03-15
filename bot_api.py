from flask import Flask, request, jsonify
import time
import random
import requests
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

app = Flask(__name__)

def setup_browser():
    options = FirefoxOptions()
    options.add_argument("--headless")  # تشغيل المتصفح بدون واجهة
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    return driver

@app.route('/register', methods=['POST'])
def register_instagram():
    driver = setup_browser()
    
    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))

        fake = Faker()
        email = fake.email()
        full_name = fake.name()
        username = fake.user_name() + str(random.randint(1000, 9999))
        password = fake.password()

        driver.find_element(By.NAME, "emailOrPhone").send_keys(email)
        driver.find_element(By.NAME, "fullName").send_keys(full_name)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

        time.sleep(5)

        return jsonify({"status": "success", "username": username, "email": email, "password": password})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
