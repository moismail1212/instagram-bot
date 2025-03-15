import time
import random
import requests
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

# 🔥 API لحل reCAPTCHA
CAPTCHA_API_KEY = "be0b601085e0248db65f2607335f9e4e"

# ========== 1. إعداد المتصفح ==========
def setup_browser():
    options = FirefoxOptions()
    options.set_preference("privacy.trackingprotection.enabled", False)  # تعطيل الحماية ضد التعقب
    options.set_preference("dom.webdriver.enabled", False)  # إخفاء أن المتصفح يعمل بسيلينيوم
    options.set_preference("useAutomationExtension", False)
    options.set_preference("media.navigator.permission.disabled", True)  # تعطيل طلبات إذن الوسائط
    options.set_preference("dom.webnotifications.enabled", False)  # تعطيل الإشعارات
    options.set_preference("dom.push.enabled", False)  # تعطيل الإشعارات الفورية
    options.add_argument("--disable-popup-blocking")  # السماح بالنوافذ المنبثقة
    options.add_argument("--disable-blink-features=AutomationControlled")  # تجنب كشف سيلينيوم
    options.add_argument("--mute-audio")  # كتم الصوت

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    return driver

# ========== 2. قبول ملفات تعريف الارتباط (Cookies) ==========
def accept_cookies(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Allow essential and optional cookies')]"))).click()
        print("✅ تم قبول ملفات تعريف الارتباط بنجاح.")
    except:
        print("⚠️ لم يتم العثور على زر قبول ملفات تعريف الارتباط. قد لا يكون مطلوبًا.")

# ========== 3. توليد بريد إلكتروني مؤقت ==========
def get_temp_email():
    url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
    response = requests.get(url).json()
    return response[0]

# ========== 4. حل reCAPTCHA ==========
def solve_captcha(api_key, site_key, url):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    
    captcha_result = solver.solve_and_return_solution()
    if captcha_result:
        print("✅ تم حل reCAPTCHA بنجاح.")
        return captcha_result
    else:
        print("❌ فشل حل CAPTCHA")
        return None

# ========== 5. تسجيل حساب Instagram ==========
def register_instagram():
    driver = setup_browser()
    
    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))

        # ✅ قبول ملفات تعريف الارتباط
        accept_cookies(driver)

        fake = Faker()
        email = get_temp_email()
        full_name = fake.name()
        username = fake.user_name() + str(random.randint(1000, 9999))
        password = fake.password()

        print(f"👤 تسجيل الحساب: {username} | 📩 {email} | 🔑 {password}")

        # 📩 إدخال البيانات
        driver.find_element(By.NAME, "emailOrPhone").send_keys(email)
        driver.find_element(By.NAME, "fullName").send_keys(full_name)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        time.sleep(random.uniform(1, 3))  # ⏳ تأخير عشوائي لمحاكاة البشر
        driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

        # 🧩 التعامل مع reCAPTCHA
        captcha_result = solve_captcha(CAPTCHA_API_KEY, "6Lc...CAPTCHA_SITE_KEY...", driver.current_url)
        if captcha_result:
            driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_result}';")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

        time.sleep(10)  # انتظر لمعرفة النتيجة

    except Exception as e:
        print(f"❌ خطأ أثناء التسجيل: {e}")

    finally:
        driver.quit()

# ========== 6. تشغيل العملية ==========
register_instagram()
