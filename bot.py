import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from keep_alive import keep_alive  # تشغيل `keep_alive.py` لمنع التوقف

# تشغيل السيرفر للحفاظ على البوت شغالًا
keep_alive()

# تثبيت Google Chrome و ChromeDriver والعثور على المسار الصحيح تلقائيًا
def install_chrome():
    """تثبيت Google Chrome و ChromeDriver داخل Railway والعثور على المسار الصحيح"""
    subprocess.run("apt update -y", shell=True)
    subprocess.run("apt install -y chromium-browser", shell=True)
    subprocess.run("apt install -y chromium-chromedriver", shell=True)

    # العثور على المسار الفعلي لـ ChromeDriver
    chrome_driver_path = subprocess.run("which chromedriver", shell=True, capture_output=True, text=True).stdout.strip()
    
    if not chrome_driver_path:
        raise FileNotFoundError("⚠️ لم يتم العثور على ChromeDriver في النظام!")

    print(f"✅ تم العثور على ChromeDriver في: {chrome_driver_path}")
    return chrome_driver_path

# إعداد Selenium لاستخدام ChromeDriver الصحيح
def setup_browser():
    """إعداد متصفح Chrome داخل Railway"""
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"  # تحديد موقع Chrome داخل Railway
    options.add_argument("--headless")  # تشغيل بدون واجهة مرئية
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # استدعاء install_chrome() للحصول على المسار الصحيح
    driver_path = install_chrome()

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
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

# إغلاق المتصفح بعد انتهاء المهام
def close_browser(driver):
    driver.quit()
    print("🚀 تم إنهاء الجلسة.")

# تشغيل النظام
def run_bot():
    """تشغيل البوت لمتابعة الحسابات تلقائيًا"""
    username = os.getenv("INSTAGRAM_USERNAME")  # اسم المستخدم من المتغيرات البيئية
    password = os.getenv("INSTAGRAM_PASSWORD")  # كلمة المرور من المتغيرات البيئية
    target_accounts = ["account1", "account2", "account3"]  # قائمة الحسابات المستهدفة

    driver = setup_browser()
    login_instagram(driver, username, password)
    
    for account in target_accounts:
        follow_accounts(driver, account)

    close_browser(driver)

# تشغيل البوت عند تنفيذ الملف
if __name__ == "__main__":
    run_bot()