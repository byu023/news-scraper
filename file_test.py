import requests
from bs4 import BeautifulSoup
import csv

url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"
response = requests.get(url)
soup = BeautifulSoup(response.text, "xml")

headlines = soup.find_all("title")

with open("news.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["見出し"])
    for h in headlines[2:]:  # 最初の2件はタイトルなのでスキップ
        writer.writerow([h.text.strip()])

print("news.csvに保存しました")