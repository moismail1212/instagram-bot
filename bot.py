import os
import time

# استيراد Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# (اختياري) إذا لديك keep_alive.py تأكّد من وضعه في مشروعك
# وضعناه في try-except كي لا يتعطل الكود إن لم يكن موجودًا
try:
    from keep_alive import keep_alive
    keep_alive()
except ImportError:
    print("⚠️ لم يتم العثور على ملف keep_alive.py. يمكنك تجاهل هذا إذا لم تكن تستخدمه.")

def setup_browser():
    """
    تهيئة متصفح Chromium/Chrome في حاوية Docker.
    نستخدم المسارات الافتراضية التي تم تثبيتها داخل Dockerfile.
    """
    chrome_options = Options()
    # المسار إلى binary الخاص بـChromium
    chrome_options.binary_location = "/usr/bin/chromium"  # أو chromium-browser
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # مسار ChromeDriver الذي ثبتناه في Dockerfile
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_instagram(driver, username, password):
    """
    تسجيل الدخول إلى حساب إنستغرام
    """
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    
    # حقول الإدخال
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    # إدخال البيانات
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    print("✅ تم تسجيل الدخول بنجاح!")

def follow_account(driver, account_username):
    """
    متابعة حساب واحد محدد
    """
    driver.get(f"https://www.instagram.com/{account_username}/")
    time.sleep(5)
    try:
        follow_button = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow_button.click()
        print(f"✅ تم متابعة الحساب: {account_username}")
    except Exception as e:
        print(f"⚠️ لم يتم متابعة الحساب {account_username} (ربما متابع بالفعل أو زر المتابعة غير متاح).\nسبب الخطأ: {e}")
    time.sleep(3)

def close_browser(driver):
    """
    إغلاق المتصفح
    """
    driver.quit()
    print("🚀 تم إنهاء جلسة المتصفح.")

def run_bot():
    """
    الدالة الرئيسية لتشغيل البوت
    """
    # جلب بيانات تسجيل الدخول من متغيرات البيئة على Railway
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        raise ValueError("⚠️ يجب تعيين متغيرات البيئة INSTAGRAM_USERNAME و INSTAGRAM_PASSWORD.")

    # الحسابات المستهدفة
    target_accounts = ["account1", "account2", "account3"]

    # فتح المتصفح
    driver = setup_browser()
    
    # تسجيل الدخول
    login_instagram(driver, username, password)
    
    # متابعة كل حساب في القائمة
    for acc in target_accounts:
        follow_account(driver, acc)

    # إغلاق المتصفح
    close_browser(driver)

if __name__ == "__main__":
    run_bot()