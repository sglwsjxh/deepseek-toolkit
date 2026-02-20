from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

def filter_digits(text):
    lines = text.splitlines()
    filtered = [line for line in lines if not re.match(r'^\d+$', line.strip())]
    return "\n".join(filtered)

def clean_text(text):
    text = filter_digits(text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()

quark_path = r"D:\Apps\Quark\quark.exe"
driver_path = r"C:\Users\mark3\Desktop\code\source\chromedriver.exe"
user_data_dir = r"C:\Users\mark3\AppData\Local\Quark\User Data"

input_prompt = input("请输入要发送的消息：")

options = Options()
options.binary_location = quark_path
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
driver.get("https://chat.deepseek.com/")

textarea = driver.find_element(By.CSS_SELECTOR, "textarea")
textarea.send_keys(input_prompt)
textarea.send_keys(Keys.RETURN)

max_wait = 300

print("\n-----------------\n思考中...\n")
first_stable_count = 0
first_previous_text = ""
first_start_time = time.time()

while time.time() - first_start_time < max_wait:
    elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
    if len(elements) >= 1:
        current_text = clean_text(elements[0].text)
        if current_text and current_text == first_previous_text:
            first_stable_count += 1
            if first_stable_count >= 3:
                print(current_text)
                break
        else:
            first_stable_count = 0
        first_previous_text = current_text
    time.sleep(1)

print("\n-----------------\n回答中...\n")
second_stable_count = 0
second_previous_text = ""
second_start_time = time.time()

while time.time() - second_start_time < max_wait:
    elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
    if len(elements) >= 2:
        current_text = clean_text(elements[1].text)
        if current_text and current_text == second_previous_text:
            second_stable_count += 1
            if second_stable_count >= 3:
                print(current_text)
                break
        else:
            second_stable_count = 0
        second_previous_text = current_text
    time.sleep(1)

driver.quit()