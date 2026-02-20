from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

quark_path = r"D:\Apps\Quark\quark.exe"
driver_path = r"C:\Users\mark3\Desktop\code\source\chromedriver.exe"
user_data_dir = r"C:\Users\mark3\AppData\Local\Quark\User Data"

options = Options()
options.binary_location = quark_path

options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

driver.get("https://chat.deepseek.com/")