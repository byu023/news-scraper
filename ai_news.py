import anthropic
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()

# ニュース見出しを取得
url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"
response = requests.get(url)
soup = BeautifulSoup(response.text, "xml")

headlines = soup.find_all("title")
news_list = []
news_text = ""
for h in headlines[2:7]:
    title = h.text.strip()
    news_list.append(title)
    news_text += title + "\n"

print("取得した見出し：")
print(news_text)

# Claude APIで要約
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"以下のニュース見出しを3行で要約してください：\n{news_text}"}
        ]
    )
    summary = message.content[0].text
    print("AIによる要約：")
    print(summary)
except Exception as e:
    summary = "API取得エラー"
    print(f"APIエラー：{e}")

# CSVに保存
today = datetime.now().strftime("%Y-%m-%d %H:%M")
filename = "news_log.csv"

with open(filename, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for title in news_list:
        writer.writerow([today, title, summary])

print(f"\nCSVに保存しました：{filename}")
