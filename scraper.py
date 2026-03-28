import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
response = requests.get(url)
soup = BeautifulSoup(response.content, "xml")

items = soup.find_all("item")

today = datetime.now().strftime("%Y-%m-%d %H:%M")

with open("news.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["日付", "タイトル"])
    for item in items[:10]:
        title = item.find("title").text
        writer.writerow([today, title])

print("保存完了！")