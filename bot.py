import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# إذا كان لديك ملف keep_alive.py لمنع توقف السيرفر، قم باستيراده وتفعيله
try:
    from keep_alive import keep_alive
    keep_alive()
except ImportError:
    print("⚠️ لم يتم العثور على ملف keep_alive.py. تأكد من وجوده إذا كنت تحتاج إليه.")

def install_chrome():
    """
    تثبيت Google Chrome و ChromeDriver على نظام Linux (مثل منصة Railway).
    يعتمد على الأوامر apt. قد تختلف هذه الأوامر في أنظمة أخرى.
    """
    print("⏳ جارِ تثبيت Google Chrome و ChromeDriver...")
    subprocess.run("apt update -y", shell=True)
    subprocess.run("apt install -y chromium-browser", shell=True)
    subprocess.run("apt install -y chromium-chromedriver", shell=True)

    # محاولة الحصول على المسار الفعلي لبرنامج ChromeDriver
    chrome_driver_path = subprocess.run("which chromedriver", shell=True, capture_output=True, text=True).stdout.strip()
    
    if not chrome_driver_path:
        raise FileNotFoundError("⚠️ لم يتم العثور على ChromeDriver في النظام!")
    
    print(f"✅ تم العثور على ChromeDriver في: {chrome_driver_path}")
    return chrome_driver_path

def setup_browser():
    """
    تهيئة متصفح Chrome (Chromium) بالخيارات المناسبة للتشغيل بدون واجهة رسومية.
    """
    # أولاً نثبّت كروم وChromeDriver
    driver_path = install_chrome()

    # ضبط إعدادات المتصفح
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # قد يختلف المسار في بعض الأنظمة
    chrome_options.add_argument("--headless")  # التشغيل بدون واجهة مرئية
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # إنشاء خدمة وتقنية تشغيل المستعرض
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_instagram(driver, username, password):
    """
    تسجيل الدخول إلى حساب إنستغرام باستخدام بيانات الدخول (اسم المستخدم وكلمة المرور).
    """
    # افتح صفحة تسجيل الدخول
    driver.get("https://www.instagram.com/accounts/login/")
    # انتظر حتى يتم تحميل الصفحة بشكلٍ كافٍ
    time.sleep(5)
    
    # ابحث عن حقول إدخال اسم المستخدم وكلمة المرور
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    # أدخل البيانات ثم اضغط على زر الإدخال (Enter)
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # انتظر لمعالجة تسجيل الدخول
    time.sleep(5)
    print("✅ تسجيل الدخول ناجح!")

def follow_accounts(driver, account_username):
    """
    متابعة حساب مُحدد (account_username) على إنستغرام.
    """
    # انتقل إلى صفحة الحساب المراد متابعته
    driver.get(f"https://www.instagram.com/{account_username}/")
    time.sleep(5)
    
    try:
        follow_button = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow_button.click()
        print(f"✅ تم متابعة الحساب: {account_username}")
    except:
        print(f"⚠️ يبدو أن الحساب {account_username} متابع بالفعل أو أن زر المتابعة غير متاح حالياً.")
    
    time.sleep(3)

def close_browser(driver):
    """
    إغلاق المتصفح بعد انتهاء تنفيذ المهام.
    """
    driver.quit()
    print("🚀 تم إنهاء جلسة المتصفح.")

def run_bot():
    """
    تشغيل البوت لمتابعة مجموعة من الحسابات تلقائيًا.
    يعتمد على قراءة بيانات تسجيل الدخول من المتغيرات البيئية (ENV).
    """
    # احصل على بيانات تسجيل الدخول من المتغيرات البيئية
    username = os.getenv("INSTAGRAM_USERNAME")  # اسم المستخدم
    password = os.getenv("INSTAGRAM_PASSWORD")  # كلمة المرور

    # تأكد من وجود اسم المستخدم وكلمة المرور
    if not username or not password:
        raise ValueError("⚠️ يجب توفير اسم المستخدم وكلمة المرور عبر المتغيرات البيئية INSTAGRAM_USERNAME و INSTAGRAM_PASSWORD.")

    # قائمة الحسابات المراد متابعتها (قم بتعديلها حسب رغبتك)
    target_accounts = ["account1", "account2", "account3"]
    
    # تهيئة المتصفح وتسجيل الدخول
    driver = setup_browser()
    login_instagram(driver, username, password)

    # متابعة كل حساب في القائمة
    for account in target_accounts:
        follow_accounts(driver, account)

    # إغلاق المتصفح بعد الانتهاء
    close_browser(driver)

# يُشغّل البوت تلقائيًا عند تنفيذ الملف مباشرةً
if __name__ == "__main__":
    run_bot()