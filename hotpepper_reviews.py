from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import anthropic
import os
import time
import csv
from datetime import datetime

load_dotenv()

def get_reviews(url, max_pages=3):
    """ホットペッパーから複数ページのレビューを取得する"""
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    review_list = []

    for page in range(1, max_pages + 1):
        if page == 1:
            page_url = url
        else:
            page_url = url + f"PN{page}.html"

        print(f"{page}ページ目を取得中...")
        driver.get(page_url)
        time.sleep(3)

        reviews = driver.find_elements(By.CSS_SELECTOR, "p.mT10.wwbw")
        if not reviews:
            print("レビューがありません。終了します。")
            break

        for r in reviews:
            review_list.append(r.text)

    driver.quit()
    return review_list

def generate_reply(review):
    """Claude APIで返信文を生成する"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"美容サロンのオーナーとして以下の口コミに丁寧な返信を100文字以内で書いてください：\n{review}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"APIエラー：{e}"


def save_csv(results):
    """レビューと返信をCSVに保存する"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = "reviews_log.csv"
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for review, reply in results:
            writer.writerow([today, review, reply])
    print(f"CSVに保存しました：{filename}")


def main():
    url = "https://beauty.hotpepper.jp/slnH000376942/review/"
    reviews = get_reviews(url, max_pages=3)

    print(f"取得したレビュー数：{len(reviews)}件\n")
    results = []
    for i, review in enumerate(reviews):
        print(f"--- レビュー{i+1} ---")
        print(f"口コミ：{review[:50]}...")
        reply = generate_reply(review)
        print(f"返信案：{reply}")
        print()
        results.append((review, reply))

    save_csv(results)


if __name__ == "__main__":
    main()
