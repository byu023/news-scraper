import anthropic
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()


def get_news():
    """Google NewsからRSSで見出しを取得する"""
    url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    headlines = soup.find_all("title")
    news_list = []
    for h in headlines[2:7]:
        news_list.append(h.text.strip())
    return news_list


def summarize(news_list):
    """Claude APIでニュースを要約する"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    news_text = "\n".join(news_list)
    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"以下のニュース見出しを3行で要約してください：\n{news_text}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"APIエラー：{e}")
        return "API取得エラー"


def save_csv(news_list, summary):
    """ニュースと要約をCSVに保存する"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("news_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for title in news_list:
            writer.writerow([today, title, summary])
    print("CSVに保存しました：news_log.csv")


def main():
    news_list = get_news()
    print("取得した見出し：")
    for title in news_list:
        print(title)

    summary = summarize(news_list)
    print("\nAIによる要約：")
    print(summary)

    save_csv(news_list, summary)


if __name__ == "__main__":
    main()
