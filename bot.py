import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess
import subprocess

def install_chrome():
    """تثبيت Google Chrome و ChromeDriver في بيئة Railway"""
    subprocess.run("apt update", shell=True)
    subprocess.run("apt install -y chromium-chromedriver", shell=True)
    print("✅ تم تثبيت Google Chrome و ChromeDriver بنجاح!")

install_chrome()
from keep_alive import keep_alive
keep_alive()

# تثبيت Google Chrome و ChromeDriver في بيئة Railway
def install_chrome():
    subprocess.run("apt update", shell=True)
    subprocess.run("apt install -y chromium-chromedriver", shell=True)
    print("✅ تم تثبيت Google Chrome و ChromeDriver بنجاح!")

install_chrome()

# إعداد المتصفح
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_browser():
    """إعداد متصفح Chrome داخل Railway"""
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"  # تحديد مسار Google Chrome
    options.add_argument("--headless")  # تشغيل بدون واجهة مرئية
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    return driver
# تسجيل الدخول إلى إنستغرام
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)
    print("✅ تسجيل الدخول ناجح!")

# متابعة الحسابات المستهدفة
def follow_accounts(driver, target_account):
    driver.get(f"https://www.instagram.com/{target_account}/")
    time.sleep(5)
    
    try:
        follow_button = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow_button.click()
        print(f"✅ تم متابعة الحساب: {target_account}")
    except:
        print(f"⚠️ الحساب {target_account} متابع بالفعل أو زر المتابعة غير متاح.")
    
    time.sleep(3)

# إغلاق المتصفح
def close_browser(driver):
    driver.quit()
    print("🚀 تم إنهاء الجلسة.")

# تشغيل النظام
def run_bot():
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    target_accounts = ["account1", "account2", "account3"]  # قائمة الحسابات المستهدفة
    
    driver = setup_browser()
    login_instagram(driver, username, password)
    
    for account in target_accounts:
        follow_accounts(driver, account)
    
    close_browser(driver)

# تنفيذ البوت
if __name__ == "__main__":
    run_bot()