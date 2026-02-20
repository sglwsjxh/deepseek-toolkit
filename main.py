from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

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

max_time = 300
start_time = time.time()

# 第一阶段：等待思考部分稳定
print("\n思考中...")
first_stable_count = 0
first_previous_text = ""

while time.time() - start_time < max_time:
    elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
    
    if len(elements) >= 1:
        raw_text = elements[0].text
        # 按行过滤纯数字行
        lines = raw_text.splitlines()
        filtered_lines = [line for line in lines if not re.match(r'^\d+$', line.strip())]
        current_text = "\n".join(filtered_lines).strip()
        
        if current_text == first_previous_text and current_text:
            first_stable_count += 1
            if first_stable_count >= 3:
                print("\n" + current_text)
                break
        else:
            first_stable_count = 0
        
        first_previous_text = current_text
    
    time.sleep(1)

# 第二阶段：等待回答部分稳定
print("\n回答中...")
second_stable_count = 0
second_previous_text = ""

while time.time() - start_time < max_time:
    elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
    
    if len(elements) >= 2:
        raw_text = elements[1].text
        lines = raw_text.splitlines()
        filtered_lines = [line for line in lines if not re.match(r'^\d+$', line.strip())]
        current_text = "\n".join(filtered_lines).strip()
        
        if current_text == second_previous_text and current_text:
            second_stable_count += 1
            if second_stable_count >= 3:
                print("\n" + current_text)
                break
        else:
            second_stable_count = 0
        
        second_previous_text = current_text
    
    time.sleep(1)

# 最后打印所有 markdown 元素（已过滤）
markdown_elements = driver.find_elements(By.CSS_SELECTOR, ".ds-markdown")
if markdown_elements:
    for i, element in enumerate(markdown_elements, 1):
        raw_text = element.text
        lines = raw_text.splitlines()
        filtered_lines = [line for line in lines if not re.match(r'^\d+$', line.strip())]
        filtered_text = "\n".join(filtered_lines).strip()
        if filtered_text:
            print(filtered_text)

driver.quit()