from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

# options.add_experimental_option("--headless")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

driver.get("https://chat.deepseek.com/")

textarea = driver.find_element(By.CSS_SELECTOR, "textarea")
textarea.send_keys(input_prompt)
textarea.send_keys(Keys.RETURN)

import time
import re

previous_count = 0
previous_text = ""
stable_count = 0
max_time = 300
start_time = time.time()
first_printed = False
second_printed = False

while time.time() - start_time < max_time:
    elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
    count = len(elements)
    
    if count > previous_count:
        for i in range(previous_count, count):
            text = elements[i].text.strip()
            if text and not re.match(r'^\d+$', text):
                if i == 0 and not first_printed:
                    print("\n思考中...\n")
                    print(text)
                    first_printed = True
                elif i == 1 and not second_printed:
                    print("\n回答中...\n") 
                    print(text)
                    second_printed = True
        
        previous_count = count
        stable_count = 0
    
    if count >= 2:
        current_text = elements[1].text.strip()
        if re.match(r'^\d+$', current_text):
            current_text = ""
        
        if current_text == previous_text and current_text:
            stable_count += 1
            if stable_count >= 3:
                break
        else:
            stable_count = 0
        
        previous_text = current_text
    
    time.sleep(1)

markdown_elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
if markdown_elements:
    for i, element in enumerate(markdown_elements, 1):
        text_content = element.text.strip()
        if text_content:
            print(text_content)

driver.quit()