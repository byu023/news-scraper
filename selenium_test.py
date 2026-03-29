from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # ブラウザを画面に表示しない

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

print(f"タイトル：{driver.title}")
print("Selenium動作確認OK！")

driver.quit()
